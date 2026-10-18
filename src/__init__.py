import base64
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
import hashlib
import secrets
import uuid


@dataclass(frozen=True)
class SecurityControlPlane:
    """A secure control plane orchestrator for managing access tokens and stateless sessions."""

    # Configuration - immutable tenant rules
    config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.config is not None and 'keys' in self.config:
            raise ValueError("Cannot reuse existing keys. Use a fresh key for this instance.")

    @property
    def current_keys(self) -> List[Dict[str, str]]:
        """Return the list of currently active session tokens."""
        if self._active_sessions is None:
            return []
        
        # Ensure all sessions are referenced in config keys before returning
        for key_name, value in self.config.items():
            if 'keys' not in value or isinstance(value, dict):
                raise ValueError(f"Key '{key_name}' does not have a 'keys' sub-key.")

        active = [s['token'] for s in self._active_sessions]
        
        # Ensure all tokens are referenced before returning (for consistency)
        if set(active).issubset(set(self.config.keys())):
            return list(active) + list([k for k, v in self.config.items() 
                                       if 'keys' not in v or isinstance(v, dict)])

    def _generate_key_id(self) -> str:
        """Generate a unique key ID using SHA-256."""
        return hashlib.sha256(secrets.token_hex(32)).hexdigest().upper()

    def generate_session_token(self) -> Dict[str, Any]:
        """Create and return a new session token with cryptographic hashing for verification. Returns None if already active."""
        
        # Generate ephemeral key ID (simulated "ephemeral" in code without actual crypto here)
        current_key_id = self._generate_key_id()

        # Create the base session object structure
        session_data: Dict[str, Any] = {
            'token': secrets.token_urlsafe(32),  # Base64 encoded for storage/verification (simulated)
            'key_id': current_key_id,
            'tenant_id': self.config.get('tenant', 'default'),
            'user_agent': f"SecurityControlPlane_{self._generate_key_id()}",
        }

        if hasattr(self, '_active_sessions'):
            # If we have active sessions in memory (simulated), return them directly
            for s in list(self._active_sessions):
                session_data['token'] = s.get('token', '')
            
            self._active_sessions.clear()  # Clear old state to ensure fresh tokens
            
        else:
            if not isinstance(session_data, dict) or 'key_id' not in session_data:
                raise ValueError("Session token must contain a key_id field.")

        return session_data
    
    def rotate_session(self) -> Optional[Dict[str, Any]]:
        """Rotate the current active session. Returns None on success."""
        
        if self._active_sessions is None or len(list(self._active_sessions)) == 0:
            raise ValueError("No sessions to rotate.")

        # Get and return existing token for rotation (simulated)
        old_token = list(self.config.keys())[-1]
        
        new_session_data = {
            'token': secrets.token_urlsafe(32),
            'key_id': self._generate_key_id(),
            'tenant_id': self.config.get('tenant', 'default'),
            'user_agent': f"SecurityControlPlane_{self._generate_key_id()}",
        }

        # Simulate expiration (in real code, this would use a timestamp)
        expire_time = secrets.token_int(1000000000)  # ~8 hours in milliseconds
        
        self._active_sessions.remove(old_token)
        
        return new_session_data
    
    def get_active_tokens(self) -> List[Dict[str, Any]]:
        """Return a copy of the active sessions."""
        if self._active_sessions is None or len(list(self._active_sessions)) == 0:
            raise ValueError("No sessions to retrieve.")

        return list(self._active_sessions)


class SecurityControlPlaneManager(SecurityControlPlane):
    """Manages access tokens and stateless sessions per user."""

    def __init__(self, config_path: str = "src/security_control_plane.py"):
        self.config = load_config(config_path)
