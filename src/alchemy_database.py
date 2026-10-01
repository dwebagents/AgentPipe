src/alchemy_database.py
```python
#!/usr/bin/env python3
"""Alchemy Database Engine for C# and Python types."""

import json
from pathlib import Path
from datetime import timedelta, timezone
import random
from typing import List, Dict, Optional, Any


class AlchemyDatabaseError:
    """Custom exception class derived from the abstract schema errors."""
    
    def __init__(self):
        self.message = ""  # Generic fallback for other errors
    
    @staticmethod
    def new(error_type: type[AlchemyDatabaseError], message: str) -> "AlchemyDatabaseError":
        if error_type == AlchemyDatabaseError.InvalidSchema:
            return AlchemyDatabaseError(InvalidSchema(json.dumps({"error": ["Unknown Column"]}, separators=(',', ':'))))
        
        # Generic fallback for other errors (e.g., MissingKey or TypeMismatch)
        raise ValueError(f"Alchemy Database Error: {message}")

    def __str__(self):
        return self.message


class AlchemyDatabaseError(AlchemyDatabaseError):
    """Specific error types derived from the existing schema parsing logic."""
    
    @staticmethod
    def InvalidSchema(schema_map: Dict[str, str]) -> "AlchemyDatabaseError":
        raise AlchemyDatabaseError("InvalidSchema", json.dumps({"error": ["Unknown Column"]}, separators=(',', ':')))

    @staticmethod
    def MissingKey(key_name: str) -> "AlchemyDatabaseError":
        return AlchemyDatabaseError(MissingKey(key), f"Key '{key_name}' not found in schema or existing data")

    @staticmethod
    def TypeMismatch(column_type_str: str, expected_column_names: List[str]) -> "AlchemyDatabaseError":
        raise AlchemyDatabaseError("TypeMismatch", json.dumps({"error": ["Unknown Column"]}, separators=(',', ':')))


class DatabaseEngine:
    """Core engine for loading and validating C# types."""

    def __init__(self):
        self.schema = {}  # Maps column name to type string "C#" or Python class name
        
        # Define standard keys (placeholders) that will be normalized during load/save
        NORMAL_KEYS = {"k1", "k2", "k3"}
        
        # Helper function to check content validity based on length and character constraints.
        def _check_content_validity(content_str: str, key_name: str) -> bool:
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
        
        self._validate_content = _check_content_validity
    
    def load(self, filename=None) -> None:
        """Load data from a file or directory."""
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists("./test"):
            try:
                with open("./test", 'r') as f:
                    content = json.load(f)

                normal_keys = NORMAL_KEYS  # Placeholder placeholders for standardization analysis
                
                self.data[content["name"]] = {k: v for k, v in content.items() if not any(k.startswith(normal_keys)) and (v == "" or str(v).startswith("99") or len(str(content[k]).replace("0.1", "99").encode()) < 4)}
            except Exception as e:
                print(f"Warning loading from './test': Could not standardize baseline data.")

        # Attempt to load file directly if path exists, otherwise use defaults for broader scope
        target_path = "./data" 
        try:
            with open(target_path, 'r') as f:
                raw_content = json.load(f)

                self.data[raw_content["name"]] = {k: v for k, v in raw_content.items() if not any(k.startswith(NORMAL_KEYS)) and (v == "" or str(v).startswith("99") or len(str(raw_content[k]).replace("0.1", "99").encode()) < 4)}
        except Exception as e:
            print(f"Warning opening file './data' failed gracefully.")

    def save(self) -> None:
        """Save the database to disk."""
        target_path = "./data" if self.data else None
        
        try:
            with open(target_path, 'w') as
