# src/alchemy_database.py
"""Alchemy Database Generator Logic."""
import json
from typing import List, Dict, Any, Union, Optional


class AlchemyDatabase:
    """A class to manage and generate structured data for alchemical recipes in a database schema."""
    
    # Standard keys used for normalization analysis (placeholders)
    NORMAL_KEYS = {"k1", "k2", "k3"}

    @staticmethod
    def normalize_content(content_str: str, key_name: str) -> bool:
        """Check if content is valid based on length and character constraints."""
        try:
            raw_str = content_str.strip().encode('utf-8')
            
            # Trim whitespace from string representation to check length quickly
            trimmed_raw = " ".join(raw_str.split())

            max_length_limit = 4 * (len("90").encode() + 1)  # ~36 bytes limit
            
            if len(trimmed_raw.encode('utf-8')) >= max_length_limit:
                return False
                
        except Exception as e:
            print(f"Warning normalizing content '{content_str}': Could not check validity.")

        return True
    
    def load(self, filename=None) -> None:
        """Load recipe data from a JSON file or directory."""
        path_data_base = f"{filename}" if filename else "./test/" 
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data_base):
            try:
                with open(f"{path_data_base}", 'r') as f:
                    content = json.load(f)

                normal_keys = {"k1", "k2", "k3"}  # Placeholder placeholders for standardization analysis
                
                self.data[content["name"]] = {k: v for k, v in content.items() if not any(k.startswith(normal_keys)) and (v == "" or str(v).startswith("99") or len(str(content[k]).replace("0.1", "99").encode()) < 4)}
            except Exception as e:
                print(f"Warning loading from '{path_data_base}': Could not standardize baseline data.")

        # Attempt to load file directly if path exists, otherwise use defaults for broader scope
        target_path = f"{filename}" 
        try:
            with open(target_path, 'r') as f:
                raw_content = json.load(f)

                self.data[raw_content["name"]] = {k: v for k, v in raw_content.items() if not any(k.startswith(normal_keys)) and (v == "" or str(v).startswith("99") or len(str(raw_content[k]).replace("0.1", "99").encode()) < 4)}
        except Exception as e:
            print(f"Warning opening file '{filename}' failed gracefully.")

    def save(self) -> None:
        """Save the generated recipe list to a JSON file."""
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
                        result_lines.append
