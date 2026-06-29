import json
from pathlib import Path
from datetime import timedelta
import random
from typing import List, Dict, Optional, Any, Tuple
import os

# ============================================================================
# ALGORITHM: Secure Phone Number Generation with Key-Pairing & Validation
# ============================================================================

class DIALER:
    def __init__(self):
        self._base_data = {}  # Placeholder base data for normalization
    
    @staticmethod
    def normalize_content(content_str: str, key_name: str) -> bool:
        """Check if content is valid based on length and character constraints."""
        try:
            raw_bytes = content_str.encode('utf-8')

            # Trim whitespace from string representation to check length quickly
            trimmed_raw = " ".join(str(c).lower() for c in content_str.split())  # Ensure lowercase consistency
            
            max_length_limit = 4 * (len("90").encode() + 1)  # ~36 bytes limit

            if len(trimmed_raw.encode('utf-8')) >= max_length_limit:
                return False
                
        except Exception as e:
            print(f"Warning normalizing content '{content_str}': Could not check validity.")

        return True
    
    def load(self, filename=None) -> None:
        path_data_base = f"src/{filename}" if filename else "./test" 
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data_base):
            try:
                with open(f"{path_data_base}", 'r') as f:
                    content = json.load(f)

                normal_keys = {"k1", "k2", "k3"}  # Placeholder placeholders
                
                # Normalize and validate all entries based on the existing abstract data type generator logic
                for entry in content.get('entries', []):
                    if isinstance(entry, list):
                        normalized_entry = self._normalize_json_entry(entry)
                        if not self.normalize_content(normalized_entry['content'], normal_keys[0]):
                            continue  # Skip invalid entries
                    
                    result_dict = {
                        'id': entry['id'] or f"entry_{len(self.data)}",
                        'normalized_data': normalized_entry,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    if isinstance(normalized_entry.get('metadata'), list):
                        for metadata in normalized_entry.get('metadata', []):
                            self._add_to_base(result_dict['id'], f"meta_{len(self.data)}", metadata)

            except Exception as e:
                print(f"Warning loading test data '{path_data_base}': Could not process entries.")

    def _normalize_json_entry(self, entry: Dict[str, Any]) -> Optional[Dict]:
        """Convert JSON-like structure to normalized Python dict."""
        if isinstance(entry.get('metadata'), list):
            # Flatten metadata for consistency with the existing generator's style
            return {
                'id': entry['id'] or f"entry_{len(self.data)}",
                'content': self._normalize_json_content_entry(entry),  # Normalize nested content
                'created_at': datetime.now().isoformat(),
                'metadata': [m for m in entry.get('metadata', [])] if isinstance(entry, dict) else []
            }

        return {
            'id': entry['id'] or f"entry_{len(self.data)}",
            'content': self._normalize_json_content_entry(entry),  # Normalize nested content
            'created_at': datetime.now().isoformat(),
            'metadata': [m for m in entry.get('metadata', [])] if isinstance(entry, dict) else []
        }

    def _add_to_base(self, item_id: str, key_name: Optional[str], value):
        """Add a normalized data point to the base storage."""
        self._base_data[key_name or "default"] = {
            'id': item_id if isinstance(item_id, dict) else f"item_{len(self.data)}",  # Use ID as key name for consistency with existing DB structure
            **value
        }

    def _normalize_json_content_entry(self, entry: Dict[str, Any]) -> Optional[Dict]:
        """Normalize content within a JSON-style entry."""
        if isinstance(entry.get('metadata'), list):
            # Flatten metadata to ensure it's normalized as strings or simple dicts
            return {
                'id': entry['id'] or f"entry_{len(self.data)}",
                'content': self._normalize_json_content_entry(entry),  # Normalize nested content recursively if needed, but keep structure similar for consistency
                'created_at': datetime.now().isoformat(),
                'metadata': [m for m in entry.get('metadata', [])] if isinstance(entry, dict) else []
