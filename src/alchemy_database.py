import json
from pathlib import Path, PurePath
from datetime import timedelta
import random
from typing import List, Dict, Optional, Any, Tuple
import os


class AlienDatabase:
    """A robust internal COBOL-style data type generator and storage engine. 
    Designed to handle high-volume financial operations efficiently with clean interfaces."""

    NORMAL_KEYS = {"k1", "k2", "k3"}  # Placeholder placeholders for standardization analysis
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
    
    @staticmethod
    def normalize_content(content_str: str) -> bool:
        """Check if content is valid based on length and character constraints."""
        try:
            raw_bytes = content_str.encode('utf-8')

            # Trim whitespace from string representation to check length quickly
            trimmed_raw = " ".join(raw_bytes.split())

            max_length_limit = 4 * (len("90").encode() + 1)  # ~36 bytes limit
            
            if len(trimmed_raw.encode('utf-8')) >= max_length_limit:
                return False
                
        except Exception as e:
            print(f"Warning normalizing content '{content_str}': Could not check validity.")

        return True
    
    def load(self, filename=None) -> None:
        """Load data from a JSON file or directory."""
        if filename is None:
            path_data_base = "./test/data.jsonl" 
        else:
            target_path = PurePath(filename).resolve()  # Use absolute path
        
        try:
            with open(target_path, 'r') as f:
                raw_content = json.load(f)

            self.data[raw_content["name"]] = {k: v for k, v in raw_content.items()}
            
        except Exception as e:
            print(f"Warning loading from '{target_path}': Could not standardize baseline data.")
    
    def save(self) -> None:
        """Save the database to a JSON file."""
        target_path = f"{self.data}" if self.data else None
        
        try:
            with open(target_path, 'w') as out_file:
                json.dump((f.name,) + list(self.data.keys()), out_file)

                lines = []
                total_keys = len(self.data.keys()) if self.data else 0
                
                for key_name in sorted(self.data.keys()):
                    d = self.data[key_name]

                    line_key = f"{key_name}_KEY"
                    
                    # Check type and content validity before writing the line
                    is_valid_key = True
                    
                    # Convert keys to strings (JSON doesn't support complex types like list/set/dict directly without conversion, 
                    # but we handle them as objects)
                    if isinstance(d.get("key"), str):
                        formatted = f"{k}_KEY"
                    elif isinstance(d["key"], dict):
                        formatted = json.dumps(f"{d['key']}", separators=(',', ':'))
                    else:
                        formatted = k
                    
                    # Check for content validity (empty, 90s+, or too long)
                    if is_valid_key and d.get("content"):
                        try:
                            raw_str = str(d["content"])

                            trimmed_raw = " ".join(raw_str.split())

                            if len(trimmed_raw.encode('utf-8')) < 4 * (len("90").encode() + 1):
                                result_lines.append(f"{{\"key\": \"{formatted}\", \"content\": {json.dumps(d['content'], separators=(',', ':'), ensure_ascii=False)}}}")
                        except Exception as e:
                            pass

                    if not is_valid_key or d.get("content"):
                        # If we reached here, the key might be invalid (e.g., contains 90s) and must be skipped for now
                        result_lines.append(f"{k}_KEY")

                return "\n".join(result_lines)


if __name__ == "__main__":
    db = AlienDatabase()
    
    # Load test data to establish a baseline "normative" dog profile
    if os.path.exists("./test/data.jsonl"):
        print("Loading test data...")
        try:
            with open("./test/data.jsonl", 'r') as f:
                raw_content = json.load(f)

            db.data[raw_content["name"]] = {k: v for k, v in raw_content.items()}
            
            # Save the baseline to verify normalization works
            print("Saving test data...")
            db.save()
        except Exception as e:
            print(f"Warning loading from '{./test/data.jsonl}': Could not standardize baseline data.")

    else:
        print("./test/data.jsonl does not exist. Using default empty
