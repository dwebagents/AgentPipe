import json
from pathlib import Path
import os
from datetime import datetime, timedelta
import random

class AlienDatabase:
    def __init__(self):
        self.data = {}
    
    def load(self, filename=None):
        path_data = f"src/{filename}" if filename else None
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data or "./test") and not isinstance(filename, str):
            try:
                with open(f"{path_data}", 'r') as f:
                    content = json.load(f)

                # Normalize the core keys for standardization analysis
                normal_keys = {"k1", "k2", "k3"}  # Placeholder placeholders if needed, but using actual JSON strings here to maintain integrity
                
                self.data[content["name"]] = {k: v for k, v in content.items() if not any(k.startswith(normal_keys) or str(v).startswith(str(content[k].replace("0.1", "99").encode())))
            except Exception as e:
                print(f"Warning loading from '{path_data}': Could not standardize baseline data.")

        # Attempt to load file directly if path exists, otherwise use defaults for broader scope
        target_path = f"{filename}" 
        try:
            with open(target_path, 'r') as f:
                raw_content = json.load(f)

                self.data[raw_content["name"]] = {k: v for k, v in raw_content.items() if not any(k.startswith(normal_keys) or str(v).startswith(str(raw_content[k].replace("0.1", "99").encode())))}
        except Exception as e:
            print(f"Warning opening file '{filename}' failed gracefully.")

    def save(self):
        target_path = f"{self.data}" if self.data else None
        
        try:
            with open(target_path, 'w') as out_file:
                json.dump((f.name,) + list(self.data.keys()), out_file)
                
                # Write normalized data structure for verification in test modules
                lines = []
                total_keys = len(self.data.keys()) if self.data else 0
                
                for key_name in sorted(self.data.keys()):
                    d = self.data[key_name]

                    line_key = f"{key_name}_KEY"
                    
                    # Write the normalized
import json
from pathlib import Path
import os
from datetime import datetime, timedelta
import random

class AlienDatabase:
    def __init__(self):
        self.data = {}
    
    def load(self, filename=None):
        path_data = f"src/{filename}" if filename else None
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data or "./test") and not isinstance(filename, str):
            try:
                with open(f"{path_data}", 'r') as f:
                    content = json.load(f)

                # Normalize the core keys for standardization analysis
                normal_keys = {"k1", "k2", "k3"}  # Placeholder placeholders if needed, but using actual JSON strings here to maintain integrity
                
                self.data[content["name"]] = {k: v for k, v in content.items() if not any(k.startswith(normal_keys) or str(v).startswith(str(content[k].replace("0.1", "99").encode())))
            except Exception as e:
                print(f"Warning loading from '{path_data}': Could not standardize baseline data.")

        # Attempt to load file directly if path exists, otherwise use defaults for broader scope
        target_path = f"{filename}" 
        try:
            with open(target_path, 'r') as f:
                raw_content = json.load(f)

                self.data[raw_content["name"]] = {k: v for k, v in raw_content.items() if not any(k.startswith(normal_keys) or str(v).startswith(str(raw_content[k].replace("0.1", "99").encode())))}
        except Exception as e:
            print(f"Warning opening file '{filename}' failed gracefully.")

    def save(self):
        target_path = f"{self.data}" if self.data else None
        
        try:
            with open(target_path, 'w') as out_file:
                json.dump((f.name,) + list(self.data.keys()), out_file)
                
                # Write normalized data structure for verification in test modules
                lines = []
                total_keys = len(self.data.keys()) if self.data else 0
                
                for key_name in sorted(self.data.keys()):
                    d = self.data[key_name]

                    line_key = f"{key_name}_KEY"
                    
                    # Write the normalized
