src/__init__.py
"""
Security Control Plane Package v1.0.0
A self-contained implementation for generating static certificates and enforcing deployment security policies using Python's built-in `cryptography` library.
All files are signed with HMAC-SHA256 to ensure integrity before being committed or deployed.

Installation:
    pip install cryptography-cffi  # For cffi bindings if needed, but primary use is direct python code.

Usage Example:
    import src.security_control_plane as scp
    
    certs = scp.generate_certificates()
    
    for cert in certs:
        with open(cert_path) as f:
            print(f.read())

"""

from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519, dsa
from cryptography.hazmat.backends import default_backend
import os
import hashlib
import hmac
import secrets
import sys


def generate_key_pair():
    """Generate a new RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return (private_key.publickey(), private_key.private_bytes())


def generate_ecdsa_public(private_key):
    """Generate an ECDSA public key."""
    curve = ec.generate_curve(16)  # Curve name doesn't matter for self-signed certs, use a standard one like 'prime256v1' or similar in production. For this demo we'll stick to the default behavior but ensure it's consistent with our environment if possible; however, without knowing the specific curve hash used by your system (which might be different from `default_backend`), we will rely on a deterministic approach for testing purposes.
    
    # Note: In a real deployment where you have public keys stored in `.pub`, this function would use those to verify signatures against private keys. For now, it generates the key pair dynamically per instance or environment variable if available.
    return (private_key.publickey(),)


def generate_ed25519_public(private_key):
    """Generate an Ed25519 public key."""
    curve = ed25519.generate_curve(384, 0x61007b3c) # Standard ECDSA for testing purposes. In production use a specific hash like 'sha-256' or similar if your system uses its own signature algorithm (e.g., SHA-256).
    
    return curve.generate_key(publickey=private_key, private_key_bytes=None)


def generate_signature(private_key):
    """Generate an HMAC-SHA256 signature for a given message."""
    # In production, this would be called from the backend service. Here we assume you have access to the public key or can compute it if needed (though typically only one private key is used per system).
    
    msg = "Deployment verification request"  # Replace with actual data payload
    
    signature = hmac.new(
        private_key.publickey().public_bytes(), 
        bytes(msg.encode('utf-8')), 
        backend=default_backend()
    )
    return signature.signature


def verify_signature(private_key, public_key, message):
    """Verify an HMAC-SHA256 signature against a given message."""
    
    # In production: Verify with the correct key. Here we assume you have access to the private key or can compute it if needed (though typically only one is used per system).
    
    msg = "Deployment verification request"  # Replace with actual data payload
    
    expected_signature = generate_signature(private_key)
    
    return hmac.compare_digest(expected_signature, signature.signature)


def get_file_permissions(filepath):
    """Get the current file permissions of a path."""
    if os.path.exists(filepath):
        try:
            stat_info = os.stat(os.path.abspath(filepath))
            # Check for 600 (owner read/write only). In production, you might want to check the owner's group permission or full access. 
            return f"Permission={oct(stat_info.st_mode)[-3]:o}" if stat_info.st_mode & 0o400 else "Unknown"
        except OSError:
            pass
    
    # Fallback for paths that don't exist yet (shouldn't happen in a running app, but good practice)
    return f"Permission={oct(6)}"


def create_certificates():
    """Create and sign certificates using the provided key pair."""
    
    private_key = generate_key_pair()
    public_key = generate_ecdsa_public(private_key)  # Using ECDSA for self-signed certs
    
    print("Generating certificate...")
    
    cert_data = {
        "algorithm": ec.generate_curve(16),  # Use 'prime256v1
