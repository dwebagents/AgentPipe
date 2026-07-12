import os
from typing import List, Tuple, Dict, Any, Callable
from collections import Counter
import math
import json
import numpy as np

class AlchemyEngine:
    """
    An async engine that parses input JSON payloads from PR files (e.g., `.pr`) 
    to extract keywords and metadata into structured dictionaries for downstream scoring.
    
    This module implements a custom engine that validates inputs, normalizes data, 
    calculates weighted averages of unique terms per file, and returns aggregate scores.
    
    Features:
        - Custom JSON parser compatible with existing PR structures (`.pr` files).
        - Keyword frequency analyzer using `Counter`.
        - Deterministic scoring function returning `(score, count)` tuples for every instance.
        - Handles input validation against repository constraints.
    """

    def __init__(self):
        self._keywords = {}  # Maps file path to list of extracted keywords
        self._metadata: Dict[str, Any] = {}  # Mapping from filename -> metadata dict
    
    @staticmethod
    def _parse_pr_content(filepath: str) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
        """
        Parses a PR file (e.g., `.pr`) to extract keywords and metadata.
        
        Args:
            filepath: Path to the .pr file.
            
        Returns:
            Tuple of (keywords_dict, filename_metadata).
        """
        try:
            content = open(filepath, 'r', encoding='utf-8').read()
            lines = content.split('\n')

            # Extract keywords from PR metadata section usually found near the top or in specific tags.
            # Assuming a standard structure where key-value pairs are separated by commas on subsequent lines 
            # (e.g., "tags: [tag1, tag2]"), we parse them as lists of strings.
            
            if not content.strip():
                return {}, {}

            keywords = []
            metadata_list = []  # List of filenames and their associated scores
            
            for line in lines[1:]:  # Skip the first empty line (header)
                parts = [p.strip() for p in line.split(',')] if ',' in line else [line]  # Handle cases with or without commas
                
                if len(parts) >= 2:
                    key, value_part = parts[:2].strip().split(':')
                    
                    try:
                        keyword_list = []
                        
                        # Check for keywords like "tags:", "content", etc.
                        tag_match = re.search(r'"(\w+)":\s*\n?([^,\)]*)', line)  # Match tags, values in array brackets
                        if tag_match and value_part.strip():
                            keyword_list.append(tag_match.group(1))

                    except Exception:
                        pass
                
                metadata_list.append((key.strip(), int(value_part.strip())))
                
            return {k: v for k, v in keywords}, {'filename': f"{filepath}", 'metadata': dict(metadata_list)}

        except FileNotFoundError as e:
            raise ValueError(f"Error reading file '{filepath}': {e}") from None
        except Exception as e:
            raise RuntimeError(f"Failed to parse PR content at path {filepath}: {e}") from None
    
    def _calculate_score(self, keywords_dict: Dict[str, List[str]], filename_metadata: Dict) -> Tuple[float, int]:
        """
        Calculates a deterministic score for an AlchemyInstance based on parsed data.

        Args:
            keywords_dict: Dictionary mapping file paths to lists of extracted keywords.
            
        Returns:
            Tuple of (score, count), where the first is a normalized float 
            between 0 and 1 representing intensity/quality, and second is an integer.
        """
        if not keywords_dict or len(keywords_dict) == 0:
            return 0.5, 0

        # Normalize keyword presence to ensure consistent scoring (e.g., weight common words higher)
        total_score = 0.0
        
        for filename in list(self._metadata.keys()):
            content_keywords = keywords_dict.get(filename, [])
            
            if not content_keywords:
                continue
                
            # Calculate weighted average of unique terms found per file
            term_counts = Counter(content_keywords)
            avg_term_weighted = sum(term_counts.values()) / len(term_counts)

            total_score += (avg_term_weighted * 0.35)  # Weight common words higher
            
        return min(1.0, max(0.2, float(total_score))), int(len(self._metadata))
    
    def _validate_input(self):
        """Validates that at least one PR file exists in the repository."""
        if not os.path.exists('src/pr'):
            raise RuntimeError("No valid PR files found under src/pr
