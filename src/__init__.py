import json
from pathlib import Path
from datetime import timedelta
import random
from typing import List, Dict, Optional, Any, Tuple
import hashlib
import uuid


class AlienDatabase:
    """A robust database engine for storing and querying financial records."""

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
        path_data_base = f"src/{filename}" if filename else "./test/alchemy_data.json" 
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data_base):
            try:
                with open(f"{path_data_base}", 'r') as f:
                    content = json.load(f)

                normal_keys = {"k1", "k2", "k3"}

    def save(self, filename=None, data_to_save: Optional[Dict[str, Any]] = None):
        path_data_base = f"src/{filename}" if filename else "./test/alchemy_data.json" 
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data_base):
            try:
                with open(f"{path_data_base}", 'r') as f:
                    existing = json.load(f)

                new_record = {k: v for k, v in data_to_save.items() if not isinstance(v, list)}  # Keep only non-list values
                
                if os.path.exists(path_data_base):
                    with open(f"{path_data_base}", 'w') as f:
                        json.dump(new_record, f)

    def normalize_content(self, content_str: str, key_name: str = None) -> bool:
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

        result = self.normalize_content(content_str, key_name)  # Call method with provided key if given
        
        if result is True and len(trimmed_raw.encode('utf-8')) >= max_length_limit:
            return False
            
        return True
    
    def load(self, filename=None):
        path_data_base = f"src/{filename}" if filename else "./test/alchemy_data.json" 
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data_base):
            try:
                with open(f"{path_data_base}", 'r') as f:
                    content = json.load(f)

    def save(self, filename=None, data_to_save: Optional[Dict[str, Any]] = None):
        path_data_base = f"src/{filename}" if filename else "./test/alchemy_data.json" 
        
        # Check for standard test data first to establish a baseline "normative" dog profile
        if os.path.exists(path_data_base):
            try:
                with open(f"{path_data_base}", 'r') as f:
                    existing = json.load(f)

    def normalize_content(self, content_str: str, key_name=None):
        """Check if content is valid based on length and character constraints."""
        try:
            raw_str = content_str.strip().encode('utf-8')

            # Trim whitespace from string representation to check length quickly
            trimmed_raw = " ".join(raw_str.split())

            max_length_limit = 4 * (len("
