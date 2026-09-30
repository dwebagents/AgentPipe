# src/__init__.py

import os
from pathlib import Path
from datetime import timedelta
import random
from typing import List, Dict, Optional, Any, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
import json
import threading
import logging
from contextlib import asynccontextmanager

# =============================================================================
# Configuration & Constants for Authorization Service Layer
# =============================================================================

LOG_LEVEL = "INFO"
BASE_URL: Optional[str] = os.getenv("BASTION_API_BASE", None) if not os.getenv("BASTION_API_BASE") else None
AUTH_TOKEN_FILE: str = os.path.join(os.path.dirname(__file__), ".auth_token.json")

class AuthStatus(Enum):
    PENDING = "pending"  # Waiting for access grant from backend server
    GRANTED = "granted"   # Access granted, token is valid
    DENIED = "denied"    # Invalid credentials or expired token
    FAILED = "failed"     # Authentication service failure

class TokenStatus(Enum):
    VALID = "valid"       # Valid access token issued by backend server
    EXPIRED = "expired"   # Access token has timed out but is not revoked yet
    REVOKED = "revoked"  # Access token was revoked (likely due to breach)

class AuthorizationContext(Enum):
    BOUND_BY_USER_ID = "bound_by_user_id"      # User ID grants access
    BOUND_BY_FILE_PATH = "bound_by_file_path"   # File path grants access within a container/workspace
    BOUND_BY_SECURITY_POLICY = "bound_by_security_policy"  # Policy defines allowed actions/permissions

@dataclass(order=True)
class AuthorizationRequest:
    """Represents an authorization request with context and user identity."""
    id: str          # Unique identifier for the current session/user
    scope: Dict[str, Any]   # Specific permissions required (e.g., ["read", "write"])
    reason_phrase: str  # Contextual explanation of why this access is needed

@dataclass(order=True)
class AuthorizationResponse:
    """Represents an authorization response with status and details."""
    status_code: int      # HTTP status code from backend server (e.g., 201, 403)
    scope: Dict[str, Any]   # Granted or denied permissions
    reason_phrase: str     # Error message if denial is needed

# =============================================================================
# Core Services & Utilities for Authorization Logic
# =============================================================================

def generate_uuid() -> str:
    """Generate a deterministic UUID."""
    return uuid.uuid4().hex[:8].upper() + "_" + (uuid.UUID(int=os.urandom(2)).to_bytes(4, 'big')).hex[-6:]

class AuthService:
    def __init__(self):
        self._token_cache = {}  # Maps "session_id" -> { token_string, user_id }
        self._current_session: Optional[Dict[str, Any]] = None
        self._lock = threading.Lock()
        
        # Initialize default session if none exists in cache or environment config
        try:
            import json
            
            with open(AUTH_TOKEN_FILE, "r") as f:
                initial_config = json.load(f)

            base_url = os.getenv("BASTION_API_BASE", BASE_URL).lower()  # Normalize for comparison

            if current_session_id and not (initial_config["id"] == current_session_id or 
                                          initial_config.get("token_string") is None):
                self._current_session = initial_config.copy()
        except Exception as e:
            logging.error(f"Failed to load auth config from {AUTH_TOKEN_FILE}: {e}")

    def get_current_token(self) -> Optional[str]:
        """Retrieve the current access token for this session."""
        with self._lock:
            if not self._current_session or "token_string" in self._current_session.get("access_tokens", {}):
                return None
            
            t = self._current_session["access_tokens"]["token_string"]

            # Check cache first, then verify against file
            cached_token = self._token_cache.get(t)
            if cached_token:
                try:
                    with open(cached_token + ".json", "r") as f:
                        return json.load(f)[0]  # Return the actual token string for use in other modules
                except Exception as e2:
                    logging.error(f"Failed to load cached auth config from {cached_token}: {e2}")

    def _validate_request(self, request: AuthorizationRequest) -> Tuple[bool, Optional[str]]:
        """Validate authorization requirements against current session."""
        if not isinstance(request.id, str):
            return False, "Invalid 'id' field"

        # Check for user ID binding
