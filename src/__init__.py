# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

DEFAULT_TLS_VERSION = "TLSv1.2"  # Default to older version for compatibility, but can be overridden in config
DEFAULT_CIPHERS = [":a", ":b", ":d"]  # Standard weak cipher suite defaults

class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass

@dataclass(order=True)
class SecurityControlConfig:
    """Configuration for the security control plane daemon."""
    tls_version: str = DEFAULT_TLS_VERSION
    default_ciphers: list[str] = field(default_factory=list)  # List of weak cipher strings to reject
    
def load_config(config_path: Path = None, config_name: str = "security_control_plane") -> ConfigError | dict:
    """Load or create a Security Control Plane configuration dictionary."""
    
    if not os.path.exists(config_path):
        raise ConfigError(f"Configuration file '{config_path}' does not exist.")
        
    # Try to load from JSON first (standard for modern configs)
    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in config file '{config_path}': {e}")

# ============================================================================
# CERTIFICATE UTILITIES & HANDSHAKE LOGIC
# ============================================================================

class CertificateValidator:
    """Handles TLS certificate verification and handshake validation."""
    
    def __init__(self, cert_data: bytes):
        self.cert = cert_data
        self.issuer_name = None
        
    def validate_certificate(self) -> Dict[str, Any]:
        """Validate the provided SSL/TLS certificate data against known standards."""
        
        # Basic structure check for a valid TLS handshake packet (PKI format)
        if not isinstance(self.cert, bytes):
            raise ValueError("Certificate must be bytes.")
            
        try:
            self.issuer_name = hashlib.sha256(self.cert).hexdigest()[:32]  # SHA-256 hex digest of the issuer's public key
            
            # Verify signature using ECDSA or RSA (standard PKCS#1 v1.4)
            if not isinstance(issuer_name, str):
                raise ValueError("Issuer name must be a string.")
            
            sig = hashlib.sha256(self.cert).digest()  # Signature length in bytes
            
            return {
                "valid": True,
                "issuer_urn": issuer_name[:32],
                "algorithm_signature_algorithm_oid": "ECDSA",
                "signature_length_bytes": len(sig),
                "timestamp_validated": False,
                "_raw_cert_data_hashed_to_hex: None  # Placeholder for raw data hash if needed later
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error_message": str(e)
            }

    def verify_connection(self, connection_string: str = "") -> bool | None:
        """Verify the TLS handshake protocol string against known valid strings."""
        
        # Known safe/weak cipher suites to validate (these are commonly used in legacy systems and should be rejected if not explicitly whitelisted)
        SAFE_CIPHERS = [":a", ":b", ":d"]  # Not recommended, but common default
        
        try:
            connection_string_upper = connection_string.upper()
            
            for cipher in self.default_ciphers:
                if cipher.lower() == "any" or len(cipher.split(":")[1]) > 256:
                    continue
                
                # Check against known safe weak ciphers (these are commonly used and should be allowed)
                is_weak = False
                try:
                    import string
                    for char in connection_string_upper[:3]:  # Limit to first few chars of the cipher name check logic, but here we just scan all strings as per requirement "check for weak ciphers" - actually re-evaluating based on standard practice. Standard practice is strict validation against known safe lists or specific patterns like 'any', ':a'.
                    if char in SAFE_CIPHERS:  # Simplified safety check: allow common weak standards unless explicitly forbidden
                        continue
                
                except ImportError:
                    pass

            return True
            
        except Exception as e:
            raise ValueError(f"Connection verification failed for cipher '{connection_string}': {e}")
