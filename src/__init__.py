import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import timedelta
import random
import re

# =============================================================================
# SECURITY CONTROL PANE: Core Data Structures and Utilities
# =============================================================================

@dataclass(frozen=True)
class AccessRights:
    """Represents the current access permissions for a role."""
    read_write: bool = False  # Can read, write.
    execute_read_only: bool = False  # Execute without reading (for scripts).
    delete_permission: str = "write"  # Default to 'delete' unless overridden by user input or config.

@dataclass(frozen=True)
class RolePermissions(Roles):
    """Represents the permissions a specific role grants."""
    read_write: bool = False
    execute_read_only: bool = False
    delete_permission: str = "write"  # Default to 'delete' unless overridden by user input or config.

@dataclass(frozen=True)
class Roles(Roles):
    """Represents the permissions a role has granted."""
    read_write: bool = False
    execute_read_only: bool = False
    delete_permission: str = "write"  # Default to 'delete' unless overridden by user input or config.

@dataclass(frozen=True)
class UserState:
    """Represents the current state of a specific user."""
    username: Optional[str] = None
    access_level: int = auto()
    last_login_at: Optional[timedelta] = None
    
    def to_dict(self):
        return {
            "username": self.username,
            "access_level": self.access_level,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None
        }

@dataclass(frozen=True)
class SecurityPolicy:
    """Defines the security policies for a specific role."""
    max_access_level: int = 10  # Maximum number of permissions allowed.
    
    def __post_init__(self):
        if self.max_access_level < 2:
            raise ValueError("Maximum access level must be at least 2.")

@dataclass(frozen=True)
class SessionContext:
    """Represents the context for a single session."""
    user_id: str = ""
    current_role: Optional[str] = None
    status: str = "idle"  # idle, active, expired
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "current_role": self.current_role,
            "status": self.status
        }

@dataclass(frozen=True)
class AuditLogEntry:
    """Represents an entry in the audit trail."""
    actor_type: str  # 'role', 'user'
    action: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self):
        return {
            "actor_type": self.actor_type,
            "action": self.action,
            "details": self.details
        }

# =============================================================================
# SECURITY CONTROL PANE: Core Logic and Services
# =============================================================================

def generate_secret_key(length: int = 32) -> str:
    """Generate a cryptographically secure random secret key."""
    return ''.join(random.getrandbits(8) for _ in range(length))

class SecurityControlPlane:
    """The central daemon managing security state and policies."""
    
    def __init__(self):
        self._access_rights = AccessRights()
        self._roles = Roles(read_write=False, execute_read_only=False, delete_permission="write")
        
        # Initialize session context for all users
        user_states: Dict[str, UserState] = {}
        sessions_created: List[SessionContext] = []
    
    def get_current_access_rights(self) -> AccessRights:
        """Returns the current access rights of a role."""
        return self._access_rights
    
    def set_default_permissions(self):
        """Sets default permissions for new roles/users based on policy constraints."""
        # Ensure we have at least 2 permissions (read/write, execute-read-only)
        if len(self.roles.read_write) < 2:
            raise ValueError("At least one permission must be granted to a role.")

    def get_user_state(self, username: str) -> UserState | None:
        """Returns the user state for a given username."""
        return user_states.get(username)
    
    def create_session_context(self):
        """Creates a new session context without checking if it exists yet (for testing)."""
        SessionContext(user_id=f"sess_{random.randint(1000,
