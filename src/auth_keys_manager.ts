src/__init__.py
"""Security Control Plane package."""

# Security Control Plane package


import os
from typing import Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from functools import wraps
import secrets
import json
import time


@dataclass(order=True)
class AuthKeysManager(ABC):
    """Abstract base class for secure key storage and lifecycle management.

    This module provides a robust mechanism to handle encrypted string keys without exposing plaintext values outside the controlled network zone, supporting SSH, Vault integration, and other persistent mechanisms. It ensures all access tokens are validated before use in production environments.
    """

    # Configuration constants (must match your existing code)
    DEFAULT_SECRET_KEY: str = "your-secret-key"  # Replace with actual secret key path or env var if using environment variables later
    KEY_PREFIX: str = "__auth_keys__"           # Prefix for stored keys to avoid collision
    
    def __init__(self, secure_path: Optional[str] = None):
        """Initialize the manager.

        Args:
            secure_path (Optional[str]): Path or string representation of a secure storage location (e.g., Vault instance). If not provided, uses environment variables for secrets if available.
        """
        self._secure_path = secure_path or os.getenv("AUTH_KEYS_PATH", "")
        
        # Initialize key store directory structure based on path
        self._key_store_dir = Path(secure_path) if secure_path else None
        
    def _get_key_prefix(self):
        """Get the unique prefix for stored keys."""
        return f"{self.KEY_PREFIX}_".join([str(p).upper() for p in os.listdir(".")])

    @abstractmethod
    def store_key(self, key: str, value: bytes) -> bool:
        """Store a secure key-value pair.

        Args:
            key (str): The unique identifier or hash of the key to be stored. Should follow your existing naming conventions if applicable.
            value (bytes): The actual encrypted/protected data associated with this key. Must not contain plaintext values exposed during storage operations outside controlled zones.

        Returns:
            bool: True if successful, False otherwise.
        """
        pass
    
    def validate_and_store(self) -> Tuple[str, str]:
        """Validate and store a new key pair for the current session.

        This method is called on every request to ensure that all access tokens are validated before use in production environments. It retrieves stored keys from secure storage if available or uses environment variables as fallbacks.

        Returns:
            Tuple[str, str]: A tuple containing (stored_key, value) for the current session key pair.
        """
        # Validate existing keys and store new ones securely
        return self._validate_and_store()

    def _validate_and_store(self):
        """Perform secure storage of a single key or multiple keys."""
        stored_keys = []
        
        # Check if we have valid keys from previous operations (e.g., via refreshKey)
        current_key: Optional[str] = None
        
        for prev_key, value in self._get_current_session_data():
            try:
                parsed_value = json.loads(value.decode('utf-8'))
                
                # Validate the stored key format if provided by user or system (check against existing keys)
                if isinstance(parsed_value.get("key"), str):
                    unique_key_parts = [p.strip().upper() for p in os.listdir(".")[:2]]
                    
                    # Check if this is a known valid key from previous operations
                    stored_keys.append((prev_key, value))

            except (json.JSONDecodeError, ValueError) as e:
                print(f"Invalid JSON or parsing error for {parsed_value.get('key')} at index {len(stored_keys)}: {e}")
                
        # If we have valid keys from previous operations and no new user-provided key exists yet, store the current session's data directly (simplified logic)
        if stored_keys and not self._has_new_key():
            for prev_key, value in stored_keys[:]:  # Limit to first few known keys
                try:
                    parsed_value = json.loads(value.decode('utf-8'))
                    
                    # Store the current session's data (simplified logic)
                    if isinstance(parsed_value.get("key"), str):
                        unique_key_parts = [p.strip().upper() for p in os.listdir(".")[:2]]
                        
                        self._store_new_key(prev_key, parsed_value["value"])

                except json.JSONDecodeError:
                    continue
                    
        # If no valid keys found from previous operations or user-provided key exists yet, store the current session's data directly (simplified logic)
        if not stored_keys and not self._has_new_key():
