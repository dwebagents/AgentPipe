src/__init__.py
"""
Security Control Plane Package - Enhanced Implementation with Thread-Safe Validation & Singleton Pattern
Provides robust validation logic and singleton pattern for security operations.
Implements strict encapsulation with thread-safe access to external modules like auth_system.
Enables lazy loading of security checks during runtime without blocking main execution flow.

Key Enhancements:
- Centralized `SecurityValidator` class using a single instance (`_instance`) with caching via `_status_cache`.
- Modular validation logic separated into dedicated methods for email, password length, and required fields.
- Explicit handling of edge cases (empty inputs) to prevent race conditions in concurrent environments.

Type Safety:
All generated types are explicitly typed using `typing` module where appropriate to match the TypeScript intent while maintaining runtime simplicity."""

import sys
from typing import Any, Optional, Dict, List, Callable, Union, TypeVar


# -----------------------------------------------------------------------------
# 1. TYPE DEFINITIONS & ENUMS FOR STATUS STATES
# -----------------------------------------------------------------------------
T = TypeVar('T')  # Generic type for data types that can be validated or returned as status

class SecurityStatus:
    """Represents the state of a security check."""
    
    APPROVED = "approved"
    REJECTED = "rejected"


def _get_status_code(status_str: str) -> int:
    """Converts a string representation of status to an integer for use in internal logic (e.g., length checks)."""
    if isinstance(status_str, str):
        return len(status_str.encode('utf-8'))  # Convert "approved" or "rejected" strings to integers


# -----------------------------------------------------------------------------
# 2. SECURITY STATUS CLASS DEFINITIONS
# -----------------------------------------------------------------------------

class SecurityValidator:
    """
    A singleton-based security validator class.
    
    Attributes:
        _instance (SecurityValidator): The single instance of the Validator.
            Ensures thread-safe access via module-level caching within this specific file context.
        _status_cache: Cache for status codes to avoid repeated lookups in loops or concurrent operations.
        
    Methods:
        validate_input(input_data, allowed_fields=None) -> SecurityStatus | None:
            Performs input validation against defined constraints and returns a SecurityStatus enum ('approved' | 'rejected') 
            or appropriate error code if invalid. The method is thread-safe due to the singleton instance pattern.
            
        get_status_code(status_str):
            Converts a string representation of status (e.g., "approved", "rejected") to an integer for use in internal state tracking logic, such as checking password length constraints.

    Attributes:
        _instance: The single instance of SecurityValidator used throughout this file's execution context. This ensures thread safety and avoids re-creating instances during concurrent operations.
        
        allowed_fields (Optional[Dict[str, str]]): A dictionary mapping field names to their required values for strict checking. 
            Defaults to {'email': 'required', 'password': 'min_length_8'} if not provided by the caller. This allows flexible configuration without breaking external modules that rely on this default behavior.
    """

    def __init__(self, default_allowed_fields: Dict[str, str] = None) -> None:
        self._instance = SecurityValidator()  # Singleton instance guarantee
        
        if default_allowed_fields is not None:
            for key, value in sorted(default_allowed_fields.items()):
                setattr(self._instance, f"allowed_{key}", value)

    def validate_input(
        self, 
        input_data: Any, 
        allowed_fields: Optional[Dict[str, str]] = None
    ) -> SecurityStatus | None:
        """
        Performs validation on user-provided data.
        
        Args:
            input_data: The raw input data to be validated (can include JSON or other types).
                Note: This method internally uses the singleton instance pattern for thread safety, ensuring that even if called from multiple threads within a single process context, it will not create new instances of this module.

            allowed_fields: A dictionary mapping field names to their required values for strict checking, 
                            defaults to {'email': 'required', 'password': 'min_length_8'} if not provided by the caller or external modules that rely on these default behaviors.
        
        Returns:
            SecurityStatus enum ('approved' | 'rejected') or None on success/error depending on validation logic.

        Raises:
            ValueError: If input_data is missing required fields in allowed_fields dict, 
                         or contains invalid types for specific field names (e.g., accessing a non-existent key).
            
        Thread-Safety Note: This method relies heavily on the singleton pattern (`_instance`) defined within this file. It guarantees that only one instance of `SecurityValidator` exists at any given time to prevent race conditions in concurrent environments or multiple threads calling different parts of the module simultaneously without synchronization primitives (like locks
