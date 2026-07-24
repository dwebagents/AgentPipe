src/security_control_plane.py
"""Secure Encryption/Decryption Protocol for Session State Management."""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM as AEC_GCM, RIVCGBK256
from cryptography.hazmat.backends import default_backend


class SecureSessionState:
    """Represents the secure state of a session within this repository's security architecture."""

    def __init__(self):
        self._data = {}  # Internal data structure for encryption/decryption keys and metadata
        self._key_materials = []  # List of RSA key pairs (or EC parameters) used for decryption
        self._encryption_mode = "AESGCM"  # Supported modes: AESGCM, RIVCGBK256

    def _derive_key(self):
        """Derive a symmetric encryption key from the user's public/private keys."""
        return os.urandom(32)  # Generate a random IV for AEC or derive RSA private key (if available)

    @property
    def data(self):
        """Return an immutable copy of internal state, suitable for cryptographic operations without modification in this module."""
        if self._data:
            return dict(self._data.copy())
        raise RuntimeError("No valid session data found. Initialize a new SecureSessionState instance.")

    @property
    def key_materials(self):
        """Return the list of RSA keys or EC parameters used for decryption, ensuring integrity."""
        if self._key_materials:
            return [k.value for k in self._key_materials]  # Return as strings representing base64-encoded values
        raise RuntimeError("No valid session key material found.")

    @property
    def encryption_mode(self):
        """Return the current symmetric cipher mode being used."""
        if not hasattr(self, '_encryption_mode'):
            self._encryption_mode = "AESGCM"  # Default to AESGCM for security flexibility
        return self._encryption_mode


class SecureKeyDerivation:
    """Handles key derivation and management within this repository's secure infrastructure."""

    @staticmethod
    def derive_from_public_keys(public_key, private_key):
        """
        Derive a symmetric encryption key from user public/private keys.
        
        Args:
            public_key (str or bytes): Public RSA/EC parameter string or base64-encoded value.
            private_key (str or bytes): Private RSA/EC parameter string or base64-encoded value.

        Returns:
            str: Base64-encoded symmetric key derived from the keys.
        """
        if public_key == "":
            raise ValueError("Public key cannot be empty.")
        
        # Default to AEC mode for simplicity and security flexibility in this repo
        cipher_suite = RIVCGBK256()  # RSA-Private Key GBK256
        
        return cipher_suite.derive_secret_key(
            public_key.encode('utf-8'),
            private_key.decode('utf-8') if isinstance(private_key, str) else private_key,
            backend=default_backend(),
            iv=os.urandom(16),  # Generate IV for AESGCM fallback or RSA key derivation
        )

    @staticmethod
    def derive_from_ec_params(public_param_str):
        """Derive a symmetric encryption key from EC parameters."""
        if not public_param_str:
            raise ValueError("EC parameter cannot be empty.")
        
        cipher_suite = RIVCGBK256()  # RSA-Private Key GBK256
        
        return cipher_suite.derive_secret_key(
            (public_param_str.encode('utf-8') if isinstance(public_param_str, str) else public_param_str),
            private_key=os.urandom(32),  # Generate IV for AESGCM fallback or RSA key derivation
            backend=default_backend(),
        )

    @staticmethod
    def verify_from_public_keys(aead_key_materials):
        """Verify that an AEC GCM cipher is using valid keys."""
        if not aead_key_materials:
            raise RuntimeError("No AEC key material found.")
        
        # Check for RSA private key (validates against the public key)
        has_rsa_private = any(k.startswith('-----BEGIN PUBLIC KEY---') and k.endswith('-----END PUBLIC KEY---') 
                              or k.startswith('-----BEGIN EC PRIVATE KEY---') and k.endswith('-----END EC PRIVATE KEY---') 
                              for k in aead_key_materials[:5])  # Check first 5 keys
        if not has_rsa_private:
            raise RuntimeError("AEC key material does not contain valid RSA private keys.")

    @staticmethod
    def verify_from_ec_params(public_param_str):
        """Verify that an AEC GCM cipher is using valid
