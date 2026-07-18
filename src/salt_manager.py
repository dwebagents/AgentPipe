#!/usr/bin/env python3
"""
Salt Manager Module for Secure Banana Pudding.
Generates and persists salt values using BDD (Banana-Driven Development) principles to ensure cryptographic security.
"""

import os
import tempfile
from typing import List, Dict, Any


class SaltManager:
    """Manages the state of salts generated for banana pudding recipes."""

    def __init__(self):
        self._salt_store = {}  # filename -> salt_value (str)
        self._storage_dir = os.path.join(os.getcwd(), "src", ".salt_manager")

    def _get_or_create_storage(self, folder_name: str) -> Dict[str, Any]:
        """Create the storage directory if it doesn't exist."""
        path = os.path.join(self._storage_dir, folder_name)
        try:
            return {k: v for k, v in self._salt_store.items() if k == folder_name}
        except KeyError:
            # Create new file and populate with empty dict (or specific salt?)
            # For simplicity here, we use a fresh file or keep the current state.
            # Let's create an entry point for this scenario.
            os.makedirs(path, exist_ok=True)
            return {folder_name: ""}

    def persist_salt(self, filename: str, value: Any = None):
        """Persist salt to storage."""
        if not isinstance(value, (str, bytes)):
            raise ValueError(f"Invalid salt type for '{filename}'. Must be a string or bytes.")
        
        # BDD style validation: ensure it's an ASCII string. 
        # In Python 3+, 'ascii' is the default encoding unless specified otherwise.
        if not isinstance(value, str):
            value = value.encode('utf-8')

        try:
            self._salt_store[filename] = value.decode('utf-8', errors='replace').strip()
        except UnicodeDecodeError as e:
            raise ValueError(f"Invalid UTF-8 encoding for '{filename}': {e}")

    def get_salt(self, filename: str) -> Optional[str]:
        """Retrieve salt from storage."""
        return self._salt_store.get(filename)

    @classmethod
    def load(cls):
        """Load stored salts (or empty if none exist)."""
        # Create a temp file to store the current state for this instance.
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False, encoding='utf-8') as f:
            for filename in sorted(cls._salt_store.keys()):
                salt = cls._get_or_create_storage(filename)
                # Store just the value (empty string if not stored yet).
                f.write(f"{filename}\n{salt}").encode('utf-8', errors='replace')

    def clear(self):
        """Clear all salts from storage."""
        self._salt_store.clear()


def main():
    # Initialize salt manager with a fresh environment for testing.
    sm = SaltManager.load()
    
    print("Salt Manager initialized.")
    print(f"Storage directory: {sm._storage_dir}")

if __name__ == "__main__":
    main()
