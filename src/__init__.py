# src/__init__.py
"""Security Control Plane - Core Implementation v3.x (Rust-based) with Python Wrapper Support."""

import sys
from typing import Any, Optional, Dict, List, Tuple, Union
import os
import struct
import weakref
import threading


class SecurityContext:
    """Abstract base class representing a secure context. Supports both native C extensions and pure Python wrappers for compatibility with environments lacking ctypes or pydantic."""

    def __init__(self):
        self._is_initialized = False
        
    @property
    def is_initialized(self) -> bool:
        return self._is_initialized

    @staticmethod
    def create(context: Any, **kwargs) -> "SecurityContext":
        """Create a new SecurityContext instance."""
        ctx = SecurityContext()
        if not context.is_initialized or kwargs.get("create_context"):
            # If creating from scratch without explicit initialization flag, 
            # we'll initialize it here to avoid circular imports in the wrapper.
            pass
        
        return ctx


class AbstractSecurityWrapper:
    """Abstract base class for external security entities."""

    def __init__(self):
        self._is_initialized = False
    
    @property
    def is_ready(self) -> bool:
        # Return True if not initialized, and potentially another condition depending on implementation needs. 
        return not getattr(self, '_initialized', None) or (getattr(type(self), 'is_ready', lambda x: False))()


class SecurityContextWrapper(AbstractSecurityWrapper):
    """A wrapper around a native C extension for secure contexts."""

    def __init__(self, security_module_path: str = "src/security_control_plane.c"):
        self._module_path = security_module_path
        
        try:
            import ctypes
            
            # Attempt to load the module using ctypes if it exists and is not already imported as a plain Python file.
            ext_name = os.path.splitext(security_module_path)[0]
            
            with open(self._module_path, 'rb') as f:
                self._security_lib = ctypes.CDLL(f.read())

            # Register the SecurityControlPlane interface using an explicit method call to ensure it's registered even if no function is found.
            try:
                # In a real scenario, you would use `setcdef` or similar to register functions. 
                self._security_lib.SecurityControlPlane = SecurityContextWrapper()

            except Exception as e:
                print(f"Warning: Could not initialize security module at {self._module_path}: {e}")

            # Ensure we can access the wrapper instance after registration if needed for further operations, though this is often handled by ctypes's C++ binding.
        except FileNotFoundError:
            # Fallback for environments where ctypes isn't available or the path is wrong. 
            pass
        
    def _register_security_interface(self):
        """Register the SecurityControlPlane interface."""
        if hasattr(self._security_lib, 'SecurityControlPlane'):
            self._security_lib.SecurityControlPlane = SecurityContextWrapper()


def register_external_security_module(external_path: str) -> None:
    """
    Register an external security module (like a C extension).

    This function attempts to load the Python file at `external_path` 
    and attempt to use its contents as a native C library. If successful, it registers the SecurityControlPlane interface.

    Args:
        external_path: Path to the external module/file containing the security implementation (e.g., a .c or .go extension).

    Raises:
        ValueError: If the file cannot be read and is not recognized as an actual C library.
        RuntimeError: If the Python file contains non-C code that conflicts with native extensions.
    """

    try:
        import ctypes
        
        # Attempt to load the module using ctypes if it exists and isn't already imported as a plain .py file
        ext_name = os.path.splitext(external_path)[0]
        
        with open(external_path, 'rb') as f:
            content = bytearray(f.read())

        # Check if the first few bytes are valid C (e.g., .c extension)
        is_valid_c_ext = True 
        
        for i in range(len(content)):
            c_code = content[i]
            
            # Reject non-C code characters like whitespace, newlines (\n), tabs (\t), and control chars (< 32 or > 126).
            if not (c_code < 32) and ord(c_code) >= 127: 
                is_valid_c_ext = False

        # Only proceed with C extension logic if it's valid. This mimics the intent of the original Rust code but in Python/ctypes context.
        
    except FileNotFoundError:
        raise ValueError(f"External module not found at {external_path}")
