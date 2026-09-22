src/alchemy_database.py
import json
from pathlib import Path
from datetime import timedelta
import random
from typing import List, Dict, Optional, Any, Callable


class AlienDatabase:
    def __init__(self):
        self.data = {}
    
    # Define standard keys for normalization analysis (as placeholders)
    NORMAL_KEYS = {"k1", "k2", "k3"}  # Placeholder placeholders
    
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
        path_data_base = f"src/{filename}" if filename else "./test" 
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data_base):
            try:
                with open(f"{path_data_base}", 'r') as f:
                    content = json.load(f)

                normal_keys = {"k1", "k2", "k3"}

    def save(self, filename=None):
        path_data_base = f"src/{filename}" if filename else "./test" 
        
        # Save data to the database file with a timestamped key for uniqueness
        timestamp_key = str(int(datetime.datetime.now().timestamp())) + "_db_" + str(len(self.data))

        try:
            with open(f"{path_data_base}/{timestamp_key}", 'w') as f:
                json.dump({
                    "data": self.data,
                    "filename": filename or path_data_base,
                    "key_name": key_name if isinstance(key_name, str) else None,
                    "created_at": datetime.datetime.now().isoformat()
                }, f)

        except Exception as e:
            print(f"Warning saving database to {path_data_base}: Could not save data.")
