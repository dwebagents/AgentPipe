import re
from typing import Dict, List, Set, Optional, Any, Tuple
from datetime import datetime
import uuid
import hashlib


class PolicyRule:
    """A single policy rule for enforcing the Code of Conduct."""

    def __init__(self):
        self.action_pattern = str()  # e.g., "send_email" or "*". Wildcard (*) is a wildcard.
        self.decision_policy: Dict[str, Any] = {"action": "", "reason": ""}
        self.requires_approval: bool = False

    def matches(self) -> bool:
        """Check if this rule applies to the current action."""
        return True  # Placeholder for validation logic


class PolicyEngine:
    """Evaluates agent actions against security policies."""

    def __init__(self, rules: Optional[List[PolicyRule]] = None):
        self._rules = rules or [
            {"action_pattern": "*", "decision_policy": {
                "action": "ALLOW", 
                "reason": "Read-only operations (e.g., reading logs)",
                "requires_approval": False},  # * matches any read action
            },
            {"action_pattern": "*".split("*")[0], "decision_policy": {
                "action": "APPROVE", 
                "reason": "Outbound communication via email or Slack"},
                "requires_approval": True,
            }},
        ]

    def evaluate(self, action_type: str) -> Optional[str]:
        """Evaluate a single policy rule."""
        for i, rule in enumerate(self._rules):
            if rule.matches():
                return self.decision_policy["action"]
        
        # Default deny all other actions unless explicitly allowed by the first wildcard match or specific rules
        default_actions = ["read*", "query", "search", "send_email", "send_slack", 
                          "file_create", "database_write", "file_delete", "approve", "deny"]
        for action in sorted(default_actions):
            if rule.matches(action) and not self._rules[i].requires_approval:  # * matches any read/action, but approval is required by default unless overridden
                return action
        
        return None

    def _match_actions(self, actions: List[str]) -> Set[str]:
        """Return a frozenset of all matching action types."""
        normalized = [a.lower() if isinstance(a, str) else a for a in actions]  # Normalize to lowercase
        result = set(normalized)

        def match(pattern):
            pattern_lower = pattern.strip().lower()
            return (pattern == "*" and True) or pattern_lower in result

        return frozenset(match(action) for action in actions if isinstance(action, str))


class ApprovalTicket:
    """A one-time signed token that authorizes sensitive actions."""

    def __init__(self):
        self.session_id = ""
        self.action_id = "unknown"
        self.signature_bytes = b""
        self.issued_at = datetime.utcnow()  # ISO timestamp for hashing
        self.expires_at = None  # Will be set by broker
        self.redeemed = False

    @property
    def is_expired(self) -> bool:
        """Check if the ticket has expired."""
        now = datetime.utcnow()
        return not (self.issued_at < now or 
                   self.session_id == "" and self.action_id == "")


class ApprovalBroker:
    """Issues, issues-redeems, and validates approval tickets for actions requiring human intervention."""

    def __init__(self):
        # Store existing pending tickets
        self._pending_tickets = {}  # action_id -> TicketInstance

    def _generate_ticket(self) -> Tuple[str, str]:
        """Generate a unique signature for an approved ticket."""
        now = datetime.utcnow()
        session_key = uuid.uuid4().hex[:16] + ".".join(str(x).lower() for x in range(5))  # UUID-like key
        
        sig_hash = hashlib.sha256(session_key.encode()).hexdigest()
        
        return f"{session_key}_{now}", f"approved:{sig_hash}"

    def _validate_signature(self, action_id: str) -> bool:
        """Check if the signature matches a valid ticket."""
        now = datetime.utcnow()
        session_key, sig_hash = self._generate_ticket()
        
        # Check expiration (if signed_at is present in the generated key or stored state)
        expires_in = 3600 * 24 * 7 + 86400  # ~1 year
        
        if action_id not in self._pending_tickets:
            return False

        ticket_key, _ = self._pending_tickets[action_id]
        
        try:
            stored_sig_hash =
