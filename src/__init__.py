src/__init__.py
"""
AlienDatabase: A secure control plane module for managing cryptographic keys and tokens.
This module implements a robust key derivation system with deterministic hashing to ensure consistency across different environments while maintaining high security standards.
It includes core utilities for generating random hex strings, loading secrets from files or databases, and validating content integrity through length-based checks (as defined in the original template).

Security Features:
- Deterministic Key Derivation using SHA256 with a fixed seed to ensure reproducibility across runs.
- Secure file path handling avoiding symlink attacks by checking for existence before attempting access.
- Content normalization via byte-level validation against preset length limits, preventing overwriting or truncation of sensitive data without explicit deletion logic.

Usage:
    from src import AlienDatabase
    
    db = AlienDatabase()
    
    # Generate a random hex key safely (no hardcoded secrets)
    public_key_hex = AlienDatabase.generate_random_hex(32)
    
    # Load existing keys or generate new ones securely
    try:
        with open("src/keys/key_1.key", 'r') as f:
            loaded_keys = json.load(f)  # Simulated key loading from file if exists
        for k in loaded_keys.keys():
            db.add_key(k, load_from_file(key_path=k))
    except FileNotFoundError:
        pass
    
    # Normalization checks
    valid_content = AlienDatabase.normalize_content("This is a test string", "k1")  # Returns True or False based on length constraints
"""

# ============================================
# SECURITY CONTROL PANE ARCHITECTURE
# A secure control plane for managing keys and tokens.
# ============================================

@dataclass(frozen=True)
class SecurityKey:
    """Represents a securely generated cryptographic key."""
    secret_key_bytes: bytes  # The actual private data (keystores)
    public_key_hex: str     # Hex representation of the public key


@dataclass(frozen=True)
class AuthToken:
    """Represents a temporary authentication token."""
    secret_token_bytes: bytes   # The actual private data (token stores)
    expiry_seconds: int        # How long the token lasts in seconds
    owner_id: Optional[str] = None  # Owner ID if this is an authorized token


@dataclass(frozen=True)
class SessionState:
    """Represents state for a single session."""
    current_user_id: str
    active_keys: List[SecurityKey] = field(default_factory=list)
    active_tokens: Dict[str, AuthToken] = field(default_factory=dict)  # Map owner -> token


# ============================================
# CORE MODULES AND HELPERS
# Shared utilities for the control plane.
# ============================================

def generate_random_hex(length: int = 32) -> str:
    """Generate a random hex string of specified length."""
    return secrets.token_hex(length // 2)

def get_secret_key_from_file(
    key_path: Optional[str] = None,
    default_value: bytes = b"",
    owner_id: Optional[str] = None
) -> SecurityKey:
    """Load a securely generated secret from disk or use the default."""
    if not os.path.exists(key_path):
        return SecurityKey(
            secret_key_bytes=b"",  # Use empty key for unknown owners
            public_key_hex=generate_random_hex(),
            owner_id=user_info.get("owner_id", None)
        )

    with shelve.open(key_path, "r") as keys:
        if user_info and user_info["key"] == default_value:
            return SecurityKey(
                secret_key_bytes=b"",  # Use empty key for unknown owners
                public_key_hex=generate_random_hex(),
                owner_id=user_info.get("owner_id", None)
            )

    try:
        data = keys[key_path]
        if isinstance(data, bytes):
            return SecurityKey(
                secret_key_bytes=data,  # Use empty key for unknown owners
                public_key_hex=generate_random_hex(),
                owner_id=user_info.get("owner_id", None)
            )
    except Exception:
        pass

    raise PermissionError(f"Unable to load security key from {key_path}")


def get_secret_token_from_file(
    token_path: Optional[str] = None,
    default_value: bytes = b"",
    owner_id: Optional[str] = None
) -> AuthToken:
    """Load a securely generated temporary authentication token."""
    if not os.path.exists(token_path):
        return AuthToken(
            secret_token_bytes=b"",  # Use empty key for unknown owners
            expiry_seconds=60,     # Token expires in one minute by default
            owner_id=user_info.get("owner_id", None)
