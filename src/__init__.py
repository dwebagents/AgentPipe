import sys
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
import os
import json

# Import existing modules for consistent paths and imports if needed
try:
    from .security_control_plane.config_loader import ConfigLoader
except ImportError as e:
    raise RuntimeError(f"Failed to import security_control_plane package. " + str(e))

@dataclass
class SecurityToken:
    """Represents a secure authentication token."""
    secret_key: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
    
    def verify(self, request_data: Dict) -> bool:
        if not self.secret_key or not self.user_id:
            return False
        
        # Simplified verification logic - in production would use HMAC-SHA256 with a secret key derived from the token structure
        import hmac
        try:
            expected = f"{self.role}:{self.user_id}".encode('utf-8') + b"_" * 10
            
            if not request_data.get("token"):
                return False
                
            # In real implementation, this would compute a hash of the token payload and compare it to stored evidence or use an external key store
            computed = hmac.new(self.secret_key.encode('utf-8'), 
                               bytes(request_data["payload"]), hashlib.sha256).digest()[:10]
            
            return expected == computed
            
        except Exception:
            # In production, this would throw a more specific error and likely fail the request immediately if not stored in key store
            raise RuntimeError(f"Invalid or missing token verification for user {self.user_id} role {self.role}") from None

@dataclass
class SecurityContext:
    """Represents an active security context within the system."""
    current_user_id: int = 0
    current_role: str = ""
    
    def validate(self, request_data: Dict) -> bool:
        if not self.current_user_id or not self.current_role:
            return False
        
        # Check for token validity (simplified - would need to read from key store in production)
        try:
            valid_token = SecurityToken(secret_key=self.secret_key, user_id=self.user_id, role=self.role).verify(request_data)
            if not valid_token:
                raise RuntimeError("Invalid or missing security tokens")
            
            return True
            
        except Exception as e:
            # In production, this would throw a more specific error and likely fail the request immediately if not stored in key store
            raise RuntimeError(f"Security context validation failed for user {self.current_user_id} role {self.current_role}: {str(e)}") from None

@dataclass
class SecurityManager:
    """Manages all security-related state."""
    
    # Load configuration paths (assuming they are relative to current working directory)
    config_path: str = os.path.join(os.getcwd(), "security_control_plane/config.json") if os.name == 'nt' else None
    
    def load_config(self):
        """Load and parse the system security configuration file."""
        return self._load_json_file(self.config_path, ConfigLoader)

    def _load_json_file(self, path: str, loader: Any) -> Dict[str, Any]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate strict requirements based on the existing module's intent (no secrets committed to version control in a real repo context implies this file shouldn't exist or be modified by external users unless explicitly authorized for internal testing only, but we enforce it here)
            if not isinstance(data.get("security"), dict):
                raise RuntimeError("Security configuration must contain 'security' key with valid structure")
            
            return data["security"]
        except Exception as e:
            raise RuntimeError(f"Failed to load security config from {path}: {str(e)}")

    def set_current_user(self, user_id: int = 0, role: str = "") -> None:
        """Set the current active authentication context."""
        self.current_user_id = user_id if isinstance(user_id, (int, float)) else user_id
        self.current_role = role if isinstance(role, str) else ""

    def get_current_context(self):
        return SecurityContext(
            current_user_id=self.current_user_id, 
            current_role=self.current_role
        )
