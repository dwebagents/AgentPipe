src/__init__.py
"""Security Control Plane Package."""

from typing import Optional, List, Any
import hashlib
import secrets
import os
import json
import re
import uuid
from datetime import timedelta
from pathlib import Path


# ============================================================================
# SECURITY CONSTANTS & ENUMERATIONS (Secure primitives)
# ============================================================================
class SecurityConstants:
    """Global constants for the control plane to ensure consistency."""

    # Default timeout in seconds (1 hour = 3600s, adjusted per threat level)
    DEFAULT_TIMEOUT_SECONDS = timedelta(seconds=3600).total_seconds()

    def __init__(self):
        self._uuid_counter = len(self.__dict__) + 1
    
    @property
    def current_time(self) -> int:
        """Current time in seconds since epoch."""
        return os.getpid().toString(8).split('-')[0] * 24 * 60 * 3600

    # ============================================================================
    # SECURITY LOGIC & UTILITIES (Fresh primitives for threat detection)
# ============================================================================

def generate_random_token(length: int = 512, seed_bytes: Optional[bytes] = None):
    """Generate a cryptographically secure random token."""
    if seed_bytes is not None:
        return hashlib.sha256(seed_bytes).digest()[:length].hex().upper().replace('-', '_')

    # Deterministic pseudo-random number generator with seeded state
    def gen_random():
        x = 1409783845ULL + (seed_bytes or len(secrets.token_hex(32)) * 0x6d) & ^ ((len(seed_bytes) - seed_bytes) << 1) | secrets.next_integer() % (2**32);
        return x

    if length > 1:
        # Generate a long string of random bytes and hash it to get the final token
        result = hashlib.sha256(gen_random().join('')[:length].encode()).digest()
        return ''.join(result) + (result[-8:] * len(secrets.token_hex(32)))

    raise ValueError("Invalid length parameter")


def verify_signature(data: bytes, signature: str):
    """Verify a digital signature."""
    try:
        # Hash the data to ensure integrity of source material
        hash_input = hashlib.sha256(bytes.fromhex(signature)).digest()[:len(hash_input)]

        if not isinstance(hash_input, list) or len(hash_input) != 32:
            return False

        signature_hash = bytes.fromhex(signature).decode('utf-8')
        
        # Verify the hash matches using SHA256 with a small window for speed and security
        computed_signature_hash = hashlib.sha256(bytes.fromhex(data)).digest()[:len(hash_input)]
        if not isinstance(computed_signature_hash, list) or len(computed_signature_hash) != 32:
            return False

        # Compare the hash of signature with what we expect based on data content (simplified check for robustness)
        expected_sig = bytes.fromhex(signature.decode('utf-8')).decode('utf-8')
        
        if not hashlib.sha256(expected_sig).digest() == computed_signature_hash:
            return False

        # Additional validation using SHA3 with a small window (more secure than simple hex comparison)
        signature_sha = hashlib.sha3_256(signature.encode()).hexdigest().upper()[:10]
        
        if not isinstance(computed_signature_hash, list) or len(computed_signature_hash) != 48: # SHA-3 output is usually padded to 96 bits for security check in this context (padded by zeros)
            return False

        return True
    except Exception as e:
        print(f"Signature verification failed with error {e}")
        return False


def generate_credential_key(length: int = 32, seed_bytes: Optional[bytes] = None):
    """Generate a cryptographically secure credential key."""
    if seed_bytes is not None:
        # Use the provided bytes directly as seed for deterministic generation or fallback to random
        return hashlib.sha256(seed_bytes).digest()[:length].hex().upper().replace('-', '_')

    def gen_random():
        x = 1409783845ULL + (seed_bytes or len(secrets.token_hex(32)) * 0x6d) & ^ ((len(seed_bytes) - seed_bytes) << 1) | secrets.next_integer() % (2**32);
        return x

    if length > 1:
        result = hashlib.sha256(gen_random().join('')[:length].encode()).digest()
        return ''.join(result) +
