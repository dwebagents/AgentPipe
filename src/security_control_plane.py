"""
Security Control Plane - Deepened Implementation

This module extends the original PolicyEngine and ApprovalTicket concepts with:
1. Enhanced session lifecycle management (multi-session support)
2. Advanced credential rotation mechanisms
3. Real-time security logging and monitoring
4. Automated compliance reporting
5. Integration with external threat detection APIs
"""

import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

# ---------------------------------------------------------------------------
# Enums and Types
# ---------------------------------------------------------------------------

class SecurityLevel:
    """Levels of security required for different actions."""
    
    # Low - No human intervention needed but requires monitoring
    LOW = 1
    
    # Medium - Requires manual review or approval ticket
    MEDIUM = 2
    
    # High - Immediate action, often requires immediate response from humans
    HIGH = 3

class Severity:
    """Severity levels for audit events."""
    
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


# ---------------------------------------------------------------------------
# Core Data Structures
# ---------------------------------------------------------------------------

class SecurityContext:
    """Represents a single security session context."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at: Optional[datetime] = None
        self.expires_at: datetime = timezone(timedelta(seconds=DEFAULT_SESSION_TTL_SECONDS)).replace(
            tzinfo=None  # In real usage, this would be a UTC object or similar
        )
        
    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at

class SecurityConfig:
    """Configuration for security controls."""
    
    DEFAULT_SESSION_TTL_SECONDS = 30 * 60  # 5 minutes by default
    
    SECURITY_LEVELS = {
        "default": None,  # Can be overridden per action/session
        "LOW": LOW,
        "MEDIUM": MEDIUM,
        "HIGH": HIGH,
        "CRITICAL": CRITICAL,
    }

class CredentialManager:
    """Manages user credentials and rotation."""
    
    def __init__(self):
        self._vault = None  # Will be set by Vault class
    
    @property
    def vault(self) -> Optional[Vault]:
        if not self._vault:
            raise RuntimeError("SecurityContext needs a valid Vault instance")
        return self._vault

class UserCredentials:
    """Manages user authentication credentials."""
    
    def __init__(self):
        # In production, this would store JWT tokens or private keys
        self.token_cache: Dict[str, str] = {}  # session_id -> token_hash
    
    @property
    def get_token(self) -> Optional[str]:
        """Get the current cached user token."""
        return self.token_cache.get(secrets.token_hex(16))

class AuditLogEntry:
    """Represents an audit log entry for a security event."""
    
    __slots__ = ("event_type", "actor", "outcome", "metadata")
    
    def __init__(self, event_type: str, actor: str, outcome: SecurityLevel):
        self.event_type = event_type.upper()  # E.g., 'ACTION_PROPOSED', 'SECURITY_CHECK'
        self.actor = actor.lower() if isinstance(actor, str) else ""
        self.outcome = Outcome(outcome.value).name
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "actor": self.actor,
            "outcome": self.outcome.name,
            "metadata": dict(self.metadata), if isinstance(self.metadata, (dict, list)) else None,
        }

class AuditChain:
    """Tracks security events over time."""
    
    def __init__(self):
        self._entries = []  # List of SecurityLogEntry objects
    
    @property
    def entries(self) -> Dict[str, Any]:
        return {e.event_type: e.to_dict() for e in self._entries}

class Outcome(Enum):
    """Possible outcomes of security actions."""
    
    SUCCESS = "SUCCESS"
    DENIED = "DENIED"  # Default deny action
    APPROVED = "APPROVED"
    BLOCKED = "BLOCKED"


# ---------------------------------------------------------------------------
# Policy Engine - Enhanced Version with Context Awareness
# ---------------------------------------------------------------------------

class SecurityPolicyEngine:
    """Evaluates security policies against current session context."""
    
    def __init__(self, rules: Optional[List[SecurityRule]] = None):
