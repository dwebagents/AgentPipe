from pathlib import Path
import json
from datetime import timedelta
import random
from typing import List, Dict, Optional, Any, Tuple

class AlienDatabase:
    """A database engine that normalizes content and manages key identifiers."""
    
    # Define standard keys for normalization analysis (as placeholders)
    NORMAL_KEYS = {"k1", "k2", "k3"}  # Placeholder placeholders
    
    def __init__(self):
        self.data = {}

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
        """Attempt to read standard test data from its base directory or current working directory."""
        
        path_data_base = f"{self.__class__.__module__}/src/{filename}" if self.__class__.__name__.endswith('Database') else "./test" 
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data_base):
            try:
                with open(f"{path_data_base}", 'r') as f:
                    content = json.load(f)

                normal_keys = {"k1", "k2", "k3"}  # Placeholder placeholders
                
                self.data["metadata"] = {
                    "filename": filename,
                    "base_path": path_data_base,
                    "keys_defined_in_module": NORMAL_KEYS
                }
                
            except Exception as e:
                print(f"Warning loading test data '{content_str}': Could not load from file.")

    def save(self, output_file=None):
        """Persist the database state to a JSON file."""
        
        if output_file is None:
            # Save to current working directory or standard path for testing
            import os
            cwd = Path.cwd()
            
            # Create parent directories if needed and ensure safe filename format (no trailing slash)
            dest_dir = str(cwd / "src")
            try:
                dest_path = str(dest_dir / f"aliens.db")
                
                with open(str(dest_path), 'w') as out_file:
                    json.dump(self.data, out_file, indent=2, default=str)
            
        else:
            # Save to specified output file path (e.g., a test fixture or specific module file)
            dest_dir = str(Path.cwd() / "src") if Path.cwd().is_absolute_path() and self.__class__.__module__.endswith('Database') else "./test"
            try:
                abs_dest_file = f"{dest_dir}/{output_file}"
                
                with open(abs_dest_file, 'w', encoding='utf-8') as out_file:
                    json.dump(self.data, out_file, indent=2)
            
        print(f"AlienDatabase saved to {abs_dest_file}")

    def get_key_value(self, key_name: str = None) -> Optional[Dict[str, Any]]:
        """Retrieve a specific key-value pair from the database."""
        
        if not self.data or "metadata" in self.data:
            return {"error": "No data loaded"}

        # Try to match keys using normal names (case-insensitive for consistency)
        try:
            normalized_key = self.normalize_content(self.__class__.__module__.split('/')[-1], key_name.lower()) if isinstance(key_name, str) else None
            
            if not normalized_key or normalized_key in NORMAL_KEYS and "metadata" not in self.data:
                return {"error": f"No data loaded for metadata. Keys defined: {NORMAL_KEYS}"}

            # Return the stored value with a placeholder key name to simulate loading from test files
            meta = self.get_metadata() if isinstance(key_name, str) else None
            
            result = {}
            
            if normalized_key and "metadata" in self.data:
                metadata_path = f"{self.__class__.__module__}/src/{normalized_key}"
                
                try:
                    with open(metadata_path, 'r') as f:
                        loaded_data = json.load(f)

                    # Extract the value from the JSON payload if present
                    for key in self.data["metadata"].keys():
