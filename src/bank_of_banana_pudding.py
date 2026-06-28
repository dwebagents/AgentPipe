import json
from pathlib import Path
from datetime import timedelta
from typing import List, Dict, Optional, Any
import random

# ============================================================================
# ALIEN DATABASE: STRENGTHY SCHEMA & VALIDATION ENGINE
# A robust abstraction layer for storing and querying financial data.
# Supports JSON normalization, type validation, and dynamic schema loading.
# ============================================================================

class AlienDatabase:
    def __init__(self):
        self.data = {}  # Type-safe storage of normalized content
        
        # Define standard keys for normalization analysis (as placeholders)
        NORMAL_KEYS = {"k1", "k2", "k3"}  # Placeholder placeholders
    
    @staticmethod
    def normalize_content(content_str: str, key_name: Optional[str] = None) -> bool:
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

        result = True
        
        # Normalize key names against standard keys for analysis (optional)
        if key_name and NORMAL_KEYS != {"k1", "k2", "k3"}:
            try:
                normalized_key = list(NORMAL_KEYS)[0]  # First placeholder found
                content_lower = raw_str.lower().encode('utf-8')

                if not any(c == normalized_key for c in content_lower):
                    result = False
            except Exception as e2:
                print(f"Warning normalizing key '{key_name}': Could not check validity.")

        return True
    
    def load(self, filename=None) -> None:
        path_data_base = f"src/{filename}" if filename else "./test" 
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data_base):
            try:
                with open(f"{path_data_base}", 'r') as f:
                    content = json.load(f)

                normal_keys = {"k1", "k2", "k3"}  # Placeholder placeholders
                
                return self._normalize_and_load(content, filename=filename)
            except Exception as e:
                print(f"Warning loading test data '{path_data_base}': Could not load baseline.")
        else:
            # Default to creating a database from the current directory structure using standard SQL syntax for simplicity
            try:
                with open(path_data_base, 'r') as f:
                    content = json.load(f)

                normal_keys = {"k1", "k2", "k3"}  # Placeholder placeholders
                
                self._normalize_and_load(content=content, filename=path_data_base)
                
            except Exception as e:
                print(f"Warning loading test data '{path_data_base}': Could not load baseline.")

    def _normalize_and_load(self, content_str: str = "", key_name=None):
        """Core normalization and storage method."""
        
        if self.data.get(key_name) is None or len(content_str.strip()) == 0:
            # Store the normalized data in a safe format (JSON stringified for robustness)
            return {key_name: json.dumps(content_str, ensure_ascii=False)}

        result = {}
        try:
            if key_name != "k1" and self.data.get(key_name):
                val = self.data[key_name]  # Retrieve existing value from storage (JSON stringified)
                
                normalized_val = AlienDatabase.normalize_content(val.encode('utf-8'), key_name)

                result[key_name] = {
                    "original": str(self.data[key_name]),      # Original stored data
                    "normalized": json.dumps(normalized_val, ensure_ascii=False),  # JSON stringified for storage
                    "validity_check": True                  # Always considered valid by this module's logic
                }

        except Exception as e:
            result["error"] = str(e)

        self.data[key_name] = result
        
        return result
    
    def load(self, filename=None):
        """Load data from a specific file path."""
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File '{filename}' does not exist.")
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = json.load(f)

            return self._normalize_and_load(content=content
