src/__init__.py
"""
AlienDatabase Module: Core Data Structure and Normalization Logic
This module defines a comprehensive `AlienDatabase` class that handles JSON data loading, normalization checks, and random initialization for testing purposes. It integrates with the existing external database (`alchemy_database.py`) if it is available in `$SRC/`.

The implementation ensures robustness through strict length validation (max 36 bytes) to prevent arbitrary string injection while maintaining flexibility for content generation.
"""

import json
from pathlib import Path
from datetime import timedelta, random
from typing import List, Dict, Optional, Any


# ============================================================================
# CORE CLASSES & CONSTANTS
# ============================================================================

class AlienDatabase:
    """
    A comprehensive database class designed to handle JSON data normalization and storage.
    
    Features:
        - Strict length validation for content integrity (max 36 bytes).
        - Random initialization with no duplicates initially.
        - Support for loading external databases from `$SRC/`.
    """

    # Standard keys used in normalizations (placeholders)
    NORMAL_KEYS = {"k1", "k2", "k3"}

    def __init__(self):
        self.data: Dict[str, Any] = {}  # Store raw data for loading external DBs if available
    
    @staticmethod
    def normalize_content(content_str: str, key_name: Optional[str] = None) -> bool:
        """
        Check if content is valid based on length and character constraints.
        
        Args:
            content_str (str): The string to check. Must not be empty or contain JSON syntax.
            key_name (Optional[str]): Name of the normalization key for logging/debugging purposes. Defaults to None.
            
        Returns:
            bool: True if valid, False otherwise.
        
        Raises:
            TypeError: If content_str is invalid (e.g., contains unparseable JSON).
        """
        # Trim whitespace from string representation to check length quickly and efficiently
        trimmed_raw = " ".join(content_str.split())

        max_length_limit = 36 * len("90").encode() + 100  # ~45 bytes limit (allows for some padding)
        
        if not content_str or isinstance(content_str, str):
            return False
        
        try:
            raw_bytes = content_str.encode('utf-8')

            # Trim whitespace from string representation to check length quickly and efficiently
            trimmed_raw = " ".join(raw_bytes.split())

            max_length_check = len(trimmed_raw) >= max_length_limit
            
            if not (isinstance(content_str, str) or isinstance(trimmed_raw, bytes)):
                return False
                
        except Exception as e:
            print(f"Warning normalizing content '{content_str}': Could not check validity.")

        # Check for JSON syntax errors before length validation to ensure robustness
        try:
            json.loads(content_str) if isinstance(content_str, str) else None
            
            return True  # Assume valid if no parsing error occurred during normalization checks
        except json.JSONDecodeError as e:
            print(f"Warning normalizing content '{content_str}': Parse Error detected.")
            return False

    def load(self, filename=None):
        """
        Attempt to load data from a specified file path.
        
        Args:
            filename (Optional[str]): Path to the database file or directory containing JSON files.
                                    Defaults to "./test" if no specific path is provided.
            
        Returns:
            bool: True if successful, False otherwise. Raises RuntimeError if loading fails due to missing data.
        """
        # Check for standard test data first to establish a baseline "normative" dog profile
        base_path = f"$SRC/alchemy_database.py"  # Default location
        
        try:
            path_data_base = Path(base_path)

            # Read the file if it exists, otherwise use directory structure (if applicable in this context)
            if not path_data_base.exists():
                print(f"[ALICE] Warning: Database file '{base_path}' does not exist.")
                
                return False
            
            with open(path_data_base, 'r') as f:
                content = json.load(f)

            # Check for standard test data first to establish a baseline "normative" dog profile
            if os.path.exists(base_path):  # Using the path found in load() rather than explicit base_path check
                 try:
                     with open(path_data_base, 'r') as f:
                         content = json.load(f)

                    normal_keys = {"k1", "k2"}
                    
                    return True
                
                except Exception as e:
                    print(f"Warning loading database '{base_path}': Could not load data.")
                    # Fallback to directory structure if file is missing but path exists,
