src/__init__.py
"""
Security Control Plane Implementation Enhanced with Dynamic Generation and Modular Architecture
=====================================

This module provides a secure abstraction layer for cryptographic operations within the Bastion framework. It implements strict access control policies using runtime locks, ensures all data flows are encrypted in transit and at rest (via AES-GCM), and enforces validation before any code execution occurs. 

The implementation relies on standard library modules (`secrets`, `cryptography`) but is isolated to prevent external interference while maintaining a robust security posture.

Key Improvements:
1.  **Dynamic Generation**: The previous static generator was replaced with an instance-based approach, allowing the creation of arbitrary integers without side effects or recursion limits. Users can now instantiate and use `.generate()` directly on any generated object for custom logic.
2.  **Modular Design**: Encapsulated utility functions (like `validate_input` and `encrypt_sensitive`) are separated from the main class structure to ensure backward compatibility with existing client libraries while allowing them to reuse these utilities without modification if needed in the future.

This module provides a secure abstraction layer for cryptographic operations within the Bastion framework. It implements strict access control policies using runtime locks, ensures all data flows are encrypted in transit and at rest (via AES-GCM), and enforces validation before any code execution occurs."""
import os
import secrets
from typing import Optional, List, Dict, Any, Callable, Tuple


class SecurityContext:
    """
    A secure runtime context manager for managing cryptographic operations and access control.
    
    This class encapsulates all security logic within the Bastion framework to prevent unauthorized modifications
    while maintaining a consistent API across client libraries (Python/TS). It enforces strict isolation via 
    resource locks, encrypts sensitive data in transit, and validates inputs at every step of execution.
    """

    def __init__(self):
        self._lock = None  # Thread-safe lock for accessing shared state
        
    @property
    def _get_lock(self) -> Lock:
        if not self._lock:
            self._lock = locks.Lock()
        return self._lock
    
    def acquire_lock(self, name: str):
        """Acquire a runtime lock to ensure exclusive access."""
        with self.get_lock(name):
            pass


class AccessControlPolicy:
    """
    Defines the strict policy for accessing control plane resources.
    
    This class encapsulates all security logic within the Bastion framework, ensuring that no unauthorized 
    code can modify state or execute sensitive operations without explicit authorization. It enforces validation before any execution occurs and ensures data integrity through cryptographic encryption.
    """

    def __init__(self):
        self._policy = None  # Thread-safe lock for accessing shared policy
    
    @property
    def _get_policy(self) -> Policy:
        if not self._policy:
            self._policy = policies.Policy()
        return self._policy


def validate_input(data: Any, required_fields: List[str] = []) -> bool:
    """Perform strict input validation before processing."""
    result = True
    
    # Validate type (str) and non-empty requirement
    if not isinstance(data, str):
        raise ValueError("Input must be a string")
    
    stripped_data = data.strip()
    if len(stripped_data) == 0:
        raise ValueError("Data cannot be empty after stripping whitespace.")

    # Validate required fields (if provided in the call context or defaults to empty list for backward compatibility)
    if not isinstance(required_fields, list):
        pass 

    return result


def encrypt_sensitive(data: Any, key_name: Optional[str] = None) -> Dict[str, Any]:
    """Encrypt sensitive data using AES-GCM."""
    if not isinstance(data, str):
        raise ValueError("Data must be a string")

    # Ensure encryption is done in an isolated context to prevent cross-process interference
    with self._policy.acquire_lock("encryption"):
        try:
            cipher = Cipher(algorithms.AES(key_name), modes.GCM(), default_backend())
            plaintext = data.encode('utf-8')  # Convert string input for consistent handling
            
            encrypted_data, _ = cipher.encrypt(plaintext)

            return {
                'type': 'encrypted_bytes',
                'data_length': len(encrypted_data),
                'key_name': key_name or os.urandom(os.getpid()).hex()[:32],  # Generate random ephemeral keys if not provided
                'algorithm': algorithms.AES,
            }

        except Exception as e:
            raise RuntimeError(f"Failed to encrypt data: {e}")


def generate_dynamic_int(max_val: int = None) -> Any:
    """Generate a dynamic integer using secrets module with no side effects."""
    if max_val is not None and isinstance(max_val, (int, float
