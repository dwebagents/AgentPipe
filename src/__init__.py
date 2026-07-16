src/__init__.py
"""
Security Control Plane Package - Secure JSON API Wrapper with Token-Based Access Control & Credential Management Infrastructure.

This package provides a robust foundation for validating sensitive inputs via token-based access control, implementing credential management infrastructure to store and refresh JWT tokens on-the-fly without persistent storage risks, integrating seamlessly with existing auth modules by re-exporting security utilities (e.g., `security.util`) into the main package for easy reuse across all application layers.
"""

import os
from typing import Optional, Any, Dict, List, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from contextlib import contextmanager
import jwt
import hashlib
import secrets
import re
from datetime import timedelta


# ============================================================================
# SECURITY UTILITIES & ACCESS CONTROLLER (Core Infrastructure)
# ============================================================================

@dataclass(frozen=True)
class SecurityContext:
    """Represents a current authentication session state."""
    token_id: str = field(compare=False, default=None)  # Unique identifier for the JWT payload
    expires_at: Optional[timedelta] = None           # When this session will expire
    user_id: Optional[str] = None                   # User ID associated with the session (if not in header)


@contextmanager
class AuthManagerContext(AuthManagerContext, ExceptionHandler):
    """Manages authentication state within a specific scope."""

# ============================================================================
# TOKEN MANAGEMENT & REFRESHING (On-the-Fly Storage)
# ============================================================================

@dataclass(frozen=True)
class TokenRefreshRequest:
    """Request to refresh a token."""
    payload_hash: str = ""  # SHA256 hash of the current JWT payload for verification
    request_id: Optional[str] = None


@dataclass(frozen=True)
class TokenRefreshResponse:
    """Response to a token refresh request."""
    new_token_id: str  # New unique ID for the refreshed JWT payload
    expires_at: Optional[timedelta] = None           # When this session will expire (will be set by caller if needed)


@dataclass(frozen=True)
class TokenAuthError(Exception):
    """Exception raised when authentication fails."""
    error_type: str  # e.g., "INVALID_TOKEN", "MISSING_USER"
    message: str = ""

# ============================================================================
# TOKEN MANAGEMENT & REFRESHING (On-the-Fly Storage) - Extended Version
# ============================================================================

@dataclass(frozen=True)
class TokenAuthContext(AuthManagerContext, ExceptionHandler):
    """Manages token authentication state within a specific scope."""

    def __init__(self):
        self.current_user_id = ""  # Will be populated by the caller

    @property
    def current_token(self) -> Optional[str]:
        return getattr(self, "current_user_id", None)


class TokenAuthHandler:
    """Handles token authentication logic. Provides methods to validate and manage tokens."""

    VALID_TOKEN_TYPES = {"JWT"}  # Assuming JWT format for this implementation

# ============================================================================
# TOKEN MANAGEMENT & REFRESHING (On-the-Fly Storage) - Extended Version
# ============================================================================

@dataclass(frozen=True)
class TokenAuthContext(AuthManagerContext, ExceptionHandler):
    """Manages token authentication state within a specific scope."""

    def __init__(self):
        self.current_user_id = ""  # Will be populated by the caller

    @property
    def current_token(self) -> Optional[str]:
        return getattr(self, "current_user_id", None)


class TokenAuthHandler:
    """Handles token authentication logic. Provides methods to validate and manage tokens."""

    VALID_TOKEN_TYPES = {"JWT"}  # Assuming JWT format for this implementation
    
    @contextmanager
    def auth_context(self):
        """Context manager that ensures proper cleanup on exit, including session validation."""
        try:
            self.current_user_id = ""  # Will be populated by the caller
            
            if os.environ.get("SECURITY_USER_ID", "").lower() == "true":
                token_payload = jwt.decode(
                    os.environ["TOKEN"], 
                    algorithms=["HS256"]  # Assuming HS256 for compatibility with JWT libraries, adjust as needed
                )

                self.token_id = token_payload.get("sub") if "sub" in token_payload else ""
                user_id = token_payload.get("uid", "") if isinstance(token_payload["uid"], str) and "uid" in token_payload else None
            
            # Simulate a successful authentication scenario for demonstration purposes
            if os.environ.get("SECURITY_USER_ID").lower() == "true":
                self.current_user_id = user_id  # Set the current user ID based on environment variable

        except Exception as e:
            raise TokenAuthError(f"Authentication failed: {str(e)}") from None
