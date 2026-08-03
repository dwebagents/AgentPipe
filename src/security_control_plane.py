# ---------------------------------------------------------------------------
# PolicyEngine Extension: Action Execution with Dynamic Token Generation & Validation
# ---------------------------------------------------------------------------

@dataclass
class SecurityToken:
    """A reusable token that can be used across multiple sessions."""
    
    session_id: str  # The unique identifier for this specific session instance
    action_type: str   # The type of operation being performed (e.g., "send_email")
    original_action_id: str  # Original ID from the policy engine if needed
    token_hash: bytes     # SHA256 hash of a secure string representation of the key + data
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session": self.session_id,
            "action_type": self.action_type,
            "original_action_id": original_action_id if hasattr(original_action_id, 'to_dict') else None,
            "token_hash_hex": self.token_hash.hex(),
        }


class TokenManager:
    """Manages the lifecycle and distribution of security tokens."""

    def __init__(self):
        self._tokens: Dict[str, SecurityToken] = {}  # session_id -> token instance
        self._used_session_ids: set = set()
        self._lock = threading.RLock()

    @property
    def current_token(self) -> Optional[SecurityToken]:
        with self._lock:
            return next(iter(self._tokens.values())) if self._tokens else None
    
    def get_or_create_token(
        self, session_id: str, action_type: str = "send_email"
    ) -> SecurityToken:
        """
        Get a token for the current session. If no active session exists or invalid, 
        create one and return it immediately.
        
        Returns None if an error occurs (e.g., expired session).
        """
        with self._lock:
            # Check if we have any valid tokens in this session
            existing = [t for t in self._tokens.values() if t.session_id == session_id]
            
            if not existing or all(t.is_expired for t in existing):
                return None
            
            token_hash = hashlib.sha256(
                f"{session_id}:{action_type}:" + "01".encode().hex()
            ).hexdigest()[:32]  # Keep hash short and cryptographically safe

        if session_id not in self._used_session_ids:
            with self._lock:
                token = SecurityToken(
                    session_id=session_id, 
                    action_type=action_type, 
                    original_action_id=None,
                    token_hash=self.token_hash
                )
                
                # Mark as used to prevent reuse of this specific instance
                self._used_session_ids.add(session_id)

            return token
        
        # Return existing token if it's still valid (not expired or already redeemed)
        for t in existing:
            if not t.is_expired and not t.redeemed_at:  # Note: check redeem status before expiry
                return t
    
    def get_active_tokens(self, session_id: str) -> List[SecurityToken]:
        """Get all tokens with a valid expiration date that haven't been redeemed."""
        with self._lock:
            active = [t for t in self._tokens.values() 
                     if not t.is_expired and not t.redeemed_at]
            
            # Remove expired ones but keep the one with the longest expiry time (if any)
            remaining = []
            seen_ids = set(t.session_id for t in active)
            
            for token in active:
                if token.session_id in seen_ids or token.is_expired:  # Exclude already used tokens
                    continue
                
                new_expiry = datetime.utcnow() + timedelta(seconds=300)  # Limit to short TTLs
                remaining.append(token.copy())

        return list(remaining)


class ApprovalVerifier:
    """Verifies the validity of an approval signature against stored tickets."""

    def __init__(self, vault: Vault):
        self._vault = vault
    
    @property
    def signing_key(self) -> str:
        key_type = "approval:broker:hmac"
        return f"{key_type}:{vault.get_credential(key_type)}".encode("utf-8")

    def verify_signature(
        self, 
        session_id: str, 
        action_id: str, 
        signature_bytes: bytes
    ) -> bool:
        """
        Verifies that the provided HMAC signature is valid for this specific ticket.
        
        Returns True if verified successfully; False otherwise (invalid or expired).
        """
        with self._lock:
            key = self.signing_key()
            
            # Find matching ticket by brute-force search over expiry time windows
            now = datetime.utcnow()
            valid
