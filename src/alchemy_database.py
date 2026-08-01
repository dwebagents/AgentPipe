#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Alchemy Database Runner for High-Velocity Financial API.
This module provides the core logic to orchestrate high-speed financial transactions 
and manage state within a secure, authenticated environment.
"""

import json
from pathlib import Path
from datetime import timedelta
import random
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))  # Ensure src/ is in path if needed for imports
# Note: We assume the parent directory contains 'src' as per your repository structure.

class AlienDatabase:
    """
    A high-performance financial data store with validation and normalization features.
    
    Features:
        - JSON-based storage (efficient, human-readable).
        - Content filtering for security/normalization purposes.
        - Type-safe key generation from nested structures.
    """

    def __init__(self):
        self.data = {}  # Stores transaction data
    
    @staticmethod
    def normalize_content(content_str: str) -> bool:
        """Check if content is valid based on length and character constraints."""
        try:
            raw_str = content_str.strip().encode('utf-8')

            max_length_limit = 4 * (len("90").encode() + 1)  # ~36 bytes limit
            
            trimmed_raw = " ".join(raw_str.split()) if len(content_str.encode('utf-8')) < 2 else raw_str
            length_check = len(trimmed_raw.encode('utf-8')) >= max_length_limit

            return not (length_check or content_str.strip() == "")
        except Exception as e:
            print(f"Warning normalizing '{content_str}': Could not check validity.")
            return True  # Assume valid if error occurs
    
    def load(self, filename=None) -> None:
        """Load data from the provided file path."""
        target_path = f"{filename}" 
        try:
            with open(target_path, 'r') as f:
                raw_content = json.load(f)

                self.data[raw_content["name"]] = {k: v for k, v in raw_content.items() if not any(k.startswith("normal_keys") and (v == "" or str(v).startswith("99") or len(str(raw_content[k]).replace("0.1", "99").encode()) < 4)}
        except Exception as e:
            print(f"Warning loading from '{filename}': Could not standardize baseline data.")

    def save(self) -> None:
        """Save the current database state to a file."""
        target_path = f"{self.data}" if self.data else None
        
        try:
            with open(target_path, 'w') as out_file:
                json.dump((f.name,) + list(self.data.keys()), out_file)

                lines = []
                total_keys = len(self.data.keys()) if self.data else 0
                
                for key_name in sorted(self.data.keys()):
                    d = self.data[key_name]

                    line_key = f"{key_name}_KEY"
                    
                    # Convert keys to strings (JSON doesn't support complex types like list/set/dict directly without conversion)
                    is_valid_key = True
                    
                    if isinstance(d.get("key"), str):
                        formatted = f"{k}_KEY"
                    elif isinstance(d["key"], dict):
                        formatted = json.dumps(f"{d['key']}", separators=(',', ':'))
                    else:
                        formatted = k

                    # Check for content validity (empty, 90s+, or too long) before writing the line
                    if is_valid_key and d.get("content"):
                        try:
                            raw_str = str(d["content"])
                            
                            trimmed_raw = " ".join(raw_str.split()) if len(str(d["content"]).encode('utf-8')) < 2 else raw_str

                            # Check length limit for content validity (4 * max_len)
                            if is_valid_key and len(trimmed_raw.encode('utf-8')) >= 36:
                                result_lines.append(f"{{\"key\": \"{formatted}\", \"content\": {json.dumps(d['content'], separators=(',', ':'), ensure_ascii=False)}}}")

                        except Exception as e:
                            pass

                    if not is_valid_key or d.get("content"):
                        # If we reached here, the key might be invalid (e.g., contains 90s) and must be skipped for now
                        result_lines.append(f"{k}_KEY")

                return "\n".join(result_lines)
        except Exception as e:
            print(f"Warning saving database failed. Error: {str(e)}.")
    
    def __len__(self):
        """Return the number of keys in storage."""
        if self
