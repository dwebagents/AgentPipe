src/__init__.py

"""
Security Control Plane - Core Package for Automated Identity and Access Management.

This module provides a secure framework for managing user identities, permissions, 
and access control policies within an application environment. It is designed to be robust, 
compliant with security best practices (OWASP Guidelines), and extensible via the provided API layer.
"""

import os
from typing import Any, Dict, Optional, List, Callable, Union
from dataclasses import dataclass, field
import threading
import time
import secrets
import uuid
import hashlib
import json
import logging
import re
from pathlib import Path
from enum import Enum
from functools import lru_cache

# =============================================================================
# CONFIGURATION & UTILITIES
# =============================================================================

@dataclass(order=True)
class Config:
    """Configuration manager for the system environment."""
    debug_mode: bool = False  # Debug mode logging level (0-15, where higher is more verbose but slower)
    
    def __post_init__(self):
        if not self.debug_mode and not os.environ.get("DEBUG_MODE", "false").lower() == "true":
            raise RuntimeError(
                f"Debug mode requires DEBUG_MODE environment variable to be set. "
                f"Current value: {os.environ.get('DEBUG_MODE', 'false').strip().upper()}."
            )

    def get_debug_level(self) -> int:
        """Return the debug logging level as an integer (0-15)."""
        return self.debug_mode if self.debug_mode else 2 # Default to low-level for production stability


@dataclass(order=True, frozen=False)
class SystemConfig(Config):
    """Configuration manager with enhanced security and abstraction."""
    
    class AuthKeys:
        """Handles authentication key management."""
        
            def __post_init__(self):
                if not os.environ.get("AUTH_KEYS_ENABLED", "false").lower() == "true":
                    raise RuntimeError(
                        f"Authentication keys require AUTH_KEYS_ENABLED environment variable. "
                        f"Current value: {os.environ.get('AUTH_KEYS_ENABLED', 'false').strip().upper()}."
                    )

            def get_keys(self) -> List[Dict[str, str]]:
                """Retrieve and return the stored authentication keys."""
                if not os.environ.get("AUTH_KEYS_PATH", "default").lower() == "true":
                    raise RuntimeError(
                        f"Authentication keys require AUTH_KEYS_PATH environment variable. "
                        f"Current value: {os.environ.get('AUTH_KEYS_PATH', 'default').strip().upper()}."
                    )

                # Ensure path exists if it doesn't (for testing)
                auth_keys_path = Path(os.environ.get("AUTH_KEYS_PATH", ""))
                if not auth_keys_path.exists():
                    raise RuntimeError(
                        f"Authentication keys require AUTH_KEYS_PATH environment variable. "
                        f"Current value: {os.environ.get('AUTH_KEYS_PATH', 'default').strip().upper()}."
                    )

            def load(self) -> Dict[str, str]:
                """Load and return the current authentication keys."""
                if not os.environ.get("AUTH_KEYS_ENABLED", "false").lower() == "true":
                    raise RuntimeError(
                        f"Authentication keys require AUTH_KEYS_ENABLED environment variable. "
                        f"Current value: {os.environ.get('AUTH_KEYS_ENABLED', 'false').strip().upper()}."
                    )

                auth_keys_path = Path(os.environ.get("AUTH_KEYS_PATH", ""))
                
                # Ensure path exists if it doesn't (for testing)
                if not auth_keys_path.exists():
                    raise RuntimeError(
                        f"Authentication keys require AUTH_KEYS_PATH environment variable. "
                        f"Current value: {os.environ.get('AUTH_KEYS_PATH', 'default').strip().upper()}."
                    )

            def get_all(self, key_type: str = None) -> List[Dict[str, str]]:
                """Retrieve all stored keys."""
                if not os.environ.get("AUTH_KEYS_ENABLED", "false").lower() == "true":
                    raise RuntimeError(
                        f"Authentication keys require AUTH_KEYS_ENABLED environment variable. "
                        f"Current value: {os.environ.get('AUTH_KEYS_ENABLED', 'false').strip().upper()}."
                    )

                auth_keys_path = Path(os.environ.get("AUTH_KEYS_PATH", ""))
                
                # Ensure path exists if it doesn't (for testing)
                if not auth_keys_path.exists():
                    raise RuntimeError(
                        f"Authentication keys require AUTH_KEYS_PATH environment variable. "
                        f"Current value: {os.environ.get('AUTH_KEYS_PATH', 'default').strip().upper()}."
                    )

            def get_by_type(self, key_type: str) -> Optional[Dict[str, str]]:
