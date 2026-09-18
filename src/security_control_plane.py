# ---------------------------------------------------------------------------
# PolicyEngine (Enhanced Security Control Plane)
# ---------------------------------------------------------------------------

@dataclass
class Action:
    """Represents a user-defined action to be executed."""
    
    session_id: str  # Unique identifier for the underlying SSH key/session context
    type: str         # e.g., "send_email", "deploy_node"
    description: str   # Human-readable description of what this does
    
    def __post_init__(self):
        if not self.session_id or not isinstance(self.session_id, str) or len(self.session_id) < 10:
            raise ValueError("Session ID must be at least 10 characters long")


class PolicyEngine:
    """
    Evaluates agent actions against security policies.

    Returns one of: ALLOW (no action required), APPROVE (requires signed ticket), DENY (blocked).
    
    Supports policy-driven execution, where agents are restricted to specific 
    types or operations defined in the system's ruleset.
    """

    def __init__(self) -> None:
        self._rules = self._default_rules()

    @staticmethod
    def _default_rules():
        return [
            # General Actions (Allowable by default unless restricted)
            PolicyRule("send_email", Action, reason="Outbound email communication"),
            PolicyRule("send_slack", Action, reason="Outbound slack notification"),
            
            # Data Operations (Require explicit approval for sensitive actions)
            PolicyRule(
                "database_write", 
                Action, 
                requires_approval=True, 
                description="Modify database schema or data"
            ),
            PolicyRule("file_write", Action, requires_approval=True),  # State mutation
            
            # Security & Compliance (Deny unless approved for specific reasons)
            PolicyRule(
                "exfiltrate_data", 
                Action, 
                requires_approval=False, 
                description="Exfiltration of sensitive data"
            ),
            
            # Deployment Operations (High Risk - Require strict approval or deny by default)
            PolicyRule("deploy_node", Action, requires_approval=True),
            PolicyRule(
                "network_scan", 
                Action, 
                requires_approval=False,  # Scan is generally allowed unless targeted
                description="Network reconnaissance"
            ),

            # Unknown Actions (Deny for now to prevent arbitrary behavior)
            PolicyRule("*", Action, reason="Default deny"),
        ]


class ApprovalTicket:
    """One-time signed token that authorizes a sensitive action."""
    
    def __init__(self):
        self.session_id: str = ""  # Session identifier (e.g., "ssh-key-01")
        self.action_type: str     # The specific type of action being requested ("send_email", etc.)
        self.signature_bytes   : bytes = b""  # HMAC signature over session+action+expiry
        
    @property
    def is_expired(self) -> bool:
        """Check if the ticket has expired."""
        return datetime.utcnow() >= datetime.fromisoformat(
            f"{self.session_id}:{self.action_type}:" 
             "{expires_at}"  # Format expected by broker, but we store ISO for comparison purposes in logic
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert ticket to dictionary format."""
        return {
            "session_id": self.session_id,
            "action_type": self.action_type,
            "signature_bytes_hex": self.signature_bytes.hex(),  # Store hex for easy decoding if needed later
            "issued_at": datetime.utcnow().isoformat() + "+00:00",
        }


class ApprovalBroker:
    """Manages the issuance and lifecycle of one-time signed approval tickets."""

    def __init__(self, vault: Vault):
        self._vault = vault
        self._audit_log: List[Dict[str, Any]] = []  # Stores audit events for logging
        
    @staticmethod
    def _generate_signature(session_id: str, action_type: str) -> bytes:
        """Generate HMAC signature over session+action."""
        now = datetime.utcnow()
        expiry_str = f"{now}.isoformat()" + "+00:00"  # Format expected by broker
        
        message_template = (f"{session_id}:{action_type}:" + expiry_str).encode("utf-8")
        
        key = _get_credential_key(vault, "approval.broker.hmac.secret.key.id")
        
        signature = hmac.new(
            key.encode(), 
            message_template, 
            digestmod=HMAC_ALGO  # Use a strong hash algorithm like SHA256 or HMAC-SHA1/384/512 depending on needs
        ).digest()
        
        return
