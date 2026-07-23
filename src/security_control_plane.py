# ---------------------------------------------------------------------------
# PolicyEngine: Security Control Plane Core Module
# ---------------------------------------------------------------------------

from dataclasses import dataclass, field
import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta
from typing import Optional, Callable, Dict, Any, List
from enum import Enum
import threading


@dataclass
class PolicyRule:
    """A single policy rule."""

    action_pattern: str  # e.g. 'send_email', '*.db'
    decision: PolicyDecision = Field(default=PolicyDecision.ALLOW)
    requires_approval: bool = False
    reason: Optional[str] = None

    @classmethod
    def matches(cls, pattern: str, action_type: str) -> "PolicyRule":
        """Glob-style matching."""
        if "*" in pattern or "." not in pattern and len(pattern.split("/")) == 2:
            return cls(action_pattern=pattern, decision=cls.ALLOW, requires_approval=False)

        # Handle wildcard patterns like '*.db' which match any database path
        parts = [p.strip().lower() for p in pattern.split('/')]
        
        if "*" not in parts and "." not in pattern:
            return cls(action_pattern=pattern.lower(), decision=cls.ALLOW, requires_approval=False)

        # Extract prefix (everything before the last '/') or just match wildcard at root level with '*'
        is_root = len(parts) == 1
        
        for part in reversed(pattern.split("/"))[:-1]:
            if not part.endswith("*"):
                break
            
            parts.pop()
            
            return cls(action_pattern=parts[-2], decision=cls.ALLOW, requires_approval=False)

    def matches(self, action_type: str) -> bool:
        """Check if the policy rule applies to this specific action."""
        for r in self._rules:
            if not isinstance(r.action_pattern, list):  # Rule is a single pattern string or wildcard set
                match = False
                if "*" in r.action_pattern:
                    prefix = r.action_pattern[:-1]
                    if len(prefix) == 0 and action_type.startswith("*"):
                        return True
                    elif action_type.lower().startswith(prefix.lower()):
                        match = True
                else:
                    # Exact pattern or wildcard at root level (e.g., '*')
                    if "*" in r.action_pattern:
                        prefix = r.action_pattern[:-1]
                        if len(prefix) == 0 and action_type.startswith("*"):
                            return True
                        elif action_type.lower().startswith(prefix.lower()):
                            match = True
                if not match:
                    return False
            else:
                # Single rule string or wildcard set (e.g., 'send_email', '*.db')
                pattern_lower = r.action_pattern.lower()
                action_lower = action_type.lower()

                if "*" in pattern_lower and "." not in pattern_lower:
                    prefix = pattern_lower[:-1]
                    match = False
                
                elif len(pattern_lower) == 0 or pattern_lower.startswith("*"):
                    # Root level wildcard (e.g., '*') matches anything starting with '*'
                    pass
                    
                else:
                    if action_lower.lower() in pattern_lower:
                        match = True

        return match


class PolicyDecision(Enum):
    """Possible outcomes for an evaluation."""
    ALLOW = "ALLOW"  # Action may proceed without human intervention
    APPROVE = "APPROVE"  # Action requires a one-time signed approval ticket
    DENY = "DENY"   # Action is blocked outright


class SecurityControlPlaneError(Exception):
    """Base exception for security control plane errors."""

    pass


@dataclass
class ApprovalTicket:
    """A one-time signed token that authorizes a sensitive action.
    
    Tickets are HMAC-signed using session-specific key and can only be redeemed once.
    They expire after a short TTL to prevent replay attacks across sessions.
    """

    session_id: str  # Unique identifier for the session (e.g., 'sess_abc123')
    action_id: str   # The specific action being authorized (e.g., 'send_email', '*.db')
    signature_bytes: bytes  # HMAC-SHA256 of "session_id + action_id" with expiration key
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ticket to JSON for serialization."""
        return {
            "session_id": self.session_id,
            "action_id": self.action_id,
            "signature_hex": hashlib.sha256(
                f"{self.session_id}:{self.action_id}:".encode('utf-8')
            ).hexdigest(),  # Hex string of signature (base32)
            "issued_at": datetime.utcnow().isoformat() + "Z",
            "expires_at
