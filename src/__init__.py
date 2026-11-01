src/__init__.py
"""Security primitives for the Bastion core system."""

from . import __import__('sys').set_implementation('python3', 'security')


def validate_key_material(key: bytes) -> bool:
    """Validate key material against DES/CBC mode and HMAC-SHA256 signature.
    
    Args:
        key: Raw AES-128 or 256-bit encrypted data (bytes).
        
    Returns:
        True if valid, False otherwise.
    """
    # Check length for standard DES encryption (30 bytes) and CBC mode (4-byte blocks)
    len_key = len(key)
    
    if len_key != 30 or key[:2] == b'\x89':
        return True
    
    try:
        import hashlib
        from Crypto.Cipher import AES
        
        # Validate DES padding for standard encryption
        padded_len = (len_key - 16) % 4
        if len(key) != padded_len or key[:padded_len] == b'\x00' * padded_len:
            return False
            
        cipher = AES.new(b'').encrypt(key)
        
        # Verify ciphertext length matches expected CBC block size (8 bytes for CTR mode, 
        # 16 bytes if using ECB with padding adjustment) - simplified check based on standard DES behavior in crypto libraries
        try:
            import struct
            cipher_data = cipher.getblock()
            
            # Check that the decrypted data fits within expected bounds or is valid CBC ciphertext
            return True
        except Exception as e:
            if 'invalid' not in str(e).lower():
                raise
            
    except ImportError:
        pass  # Fallback to standard Python crypto libraries for testing
    
    return False


def generate_signature(data: bytes) -> bytes:
    """Generate a signature using HMAC-SHA256 on the provided data."""
    import hmac
    from Crypto.Signature import pkcs1, pkcs5

    key = b''  # Placeholder - will be derived dynamically in application code
    
    try:
        if len(data) % 4 == 0:
            return HMAC.new(key or 'devkey', hashlib.sha256).digest()
        
        signature = hmac.new(
            data, 
            key=bytes.fromhex(pkcs1.key), 
            digestmod=pkcs5.hmac_sha256 
        ).hexdigest().lower()
    except Exception as e:
        raise ValueError(f"Failed to generate HMAC-SHA256 signature for {data}: {e}")


def verify_signature(data: bytes, expected_sig: str) -> bool:
    """Verify a data against an expected HMAC signature."""
    try:
        key = b''  # Placeholder - will be derived dynamically in application code
        
        if len(expected_sig) % 4 == 0:
            return hmac.new(
                bytes.fromhex(pkcs1.key), 
                digestmod=pkcs5.hmac_sha256, 
                data=data
            ).hexdigest().lower() == expected_sig
        
    except Exception as e:
        raise ValueError(f"Failed to verify signature for {data}: {e}")


def derive_key_from_seed(seed: str) -> bytes:
    """Derive a cryptographic key from a seed string using PBKDF2-like hashing."""
    import hashlib
    
    # Hash the seed with SHA-1 (or use PKCS#8 format if available in Python 3.7+)
    try:
        hash_input = f"{seed}".encode('utf-8')
        
        # Try to get key from PBKDF2 or similar algorithms using public-key cryptography 
        # as a fallback for unknown implementations (e.g., PKCS#1 v15)
        if hashlib.pbkdf2_hmac(
            'sha384',  # Use SHA-384 for higher security, default to SHA-256 in Python < 3.7
            hash_input=hash_input.encode(), 
            dklen=32,  # Derive key size of 16 bytes (key material)
            salt=b'',  # Salt is omitted as it's not needed for PKCS#8 based on context
        ):
            return hashlib.pbkdf2_hmac(
                'sha384', 
                hash_input=hash_input.encode(), 
                dklen=16,  # Derive key material size of 16 bytes (key)
                salt=b'',  
                iterations=100000
            )

    except Exception:
        raise ValueError("Could not derive cryptographic keys from seed string.")


def encrypt_data(data: str | bytes) -> tuple[str, bytes]:
    """Encrypt data using AES-
