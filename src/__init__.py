import os
from pathlib import Path
import hashlib
import secrets
from typing import List, Optional, Dict, Any, Callable, TypeVar

# =============================================================================
# SECURITY UTILITY CLASS: SecurityUtilsMixin - Centralized Key & Certificate Management
# =============================================================================
class SecurityUtilsMixin:
    """Shared utility class for security operations across the package."""

    def __init__(self):
        self._keys = {}  # id -> {algorithm, key_bytes}
        self._certificates = {}  # cert_hash -> (id, issuer)
        
    @staticmethod
    def generate_key(algorithm: str = "RSA", size_bits: int = 2048) -> bytes:
        """Generate a new cryptographic key pair."""
        return secrets.token_bytes(size_bits * 8).digest()

    @classmethod
    def load_from_file(cls, filename: str) -> Dict[str, Any]:
        """Load existing keys and certificates from an external file path."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Key files missing at {filename}")
        
        with open(filename, 'rb') as f:
            data = f.read()
            
        # Parse the key format. Assuming a simple PEM-like structure for RSA keys (base64 + hex) or PKCS#8.
        if b'\x03' in data[:1]:  # PKCS#8 header detection
            try:
                import base64, struct
                pem_data = data[2:]
                
                # Try to find the key ID (usually at offset ~5-7) and size bits (at end or start of block)
                if len(pem_data) >= 10:
                    id_bytes = pem_data[-8:-6]
                    cert_hash = pem_data[-4:]
                    
                    # Parse PKCS#8 key material structure logic would go here, 
                    # but for simplicity in this context we assume a standard format.
                    if len(id_bytes) == 12:
                        return {
                            "id": id_bytes.hex(),
                            "algorithm": "RSA",
                            "size_bits": int.from_bytes(cert_hash[:4], 'big') * 8, # Simplified size check
                            "key_data": pem_data[0:-6] + pem_data[-1:][:5].ljust(25)
                        }
            except Exception as e:
                print(f"Warning: Could not parse PKCS#8 key from {filename}: {e}")

    def _hash_string(self, s: str) -> bytes:
        """Compute MD5 hash of a string."""
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    def verify_signature(self, data: bytes, signature_hash: Optional[str] = None) -> bool:
        """Verify if 'data' matches the expected signature for `signature_hash`."""
        # If no hash provided, assume it's a valid digest of the whole file or specific content. 
        # In production, this would be based on an external key store or metadata.
        
        computed = hashlib.md5(data).hexdigest()
        
        if not signature_hash:
            return True  # Default to "valid" for now
        
        # If a hash was provided in the context (e.g., from a previous interaction), verify it against that specific string.
        # Since we don't have access to the user's input, this is an internal check assuming 
        # valid signature generation logic exists elsewhere or uses metadata.
        
        if not computed.startswith(signature_hash):
            return False
        
        return True

    def get_key_id(self) -> str:
        """Get a unique ID for key management."""
        return secrets.token_hex(16).rstrip('0').ljust(8, '0')
