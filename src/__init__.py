src/__init__.py


"""Security Control Plane - HTTP/2 Secure Channel Framing with TLS 1.3 Support."""

import base64
import hashlib
import hmac
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional
import ssl
from pathlib import Path


class SecurityControlPlane:
    """
    Implements a secure channel framing layer for the Control Plane.
    
    This module provides:
    1. TLS/HTTPS initialization with automatic certificate loading from environment variables or local config.
    2. HTTP/2 frame encapsulation using Base64 encoded frames (RFC 8795).
    3. HMAC-SHA256 integrity verification before encryption/authentication of data payloads.
    
    Security Features:
    - Zero-Knowledge Protocol Layer (ZKPL) support for message authentication and confidentiality.
    - RSA Key Derivation from pre-shared secrets or environment variables if not configured otherwise.
    - Secure channel framing over HTTP/2 with proper bidirectional encryption.
    """

    def __init__(self, base_url: str = "http://localhost", debug_mode: bool = False):
        self.base_url = Path(base_url).resolve()
        
        # Configuration paths for TLS keys and certificates
        tls_config_path = self.base_url / "tls"
        if not (tls_config_path.exists() or any(tls_config_path.parent.is_dir() for dir_path in [Path("conf"), Path("config")])):
            raise RuntimeError(
                f"The Security Control Plane requires configuration files to be placed at {self.base_url}/tls/ or its parent directory."
            )

        # TLS Configuration Dictionary
        self.tls_config = {}
        
        # Pre-shared secrets for key derivation (if RSA is not configured)
        self.pre_shared_secrets: dict[str, str] = {}
        
        if debug_mode:
            print("Initializing Security Control Plane with Debug Mode...")

    def load_tls_config(self):
        """Load TLS configuration from environment variables or local config files."""
        # Load env vars first (highest priority)
        for key in ["TLS_CERT_PATH", "TLS_KEY_FILE", "SSL_CAPTCHA_ENABLED"]:
            if key in self.tls_config:
                print(f"Using environment variable {key}...")
                return

        # Try local config files
        try:
            tls_path = Path("tls").joinpath(key)
            
            # If it's a directory, look for specific subdirectories or root certs/keys. 
            # For this implementation, we assume the key file is at 'config/key.pem' and cert at 'certs/cert.pem'.
            if (key == "TLS_CERT_PATH" and tls_path.exists() and not any(tls_config_path / x.name for x in ["tls", "conf"])):
                raise RuntimeError(f"The TLS configuration directory '{tls_path}' is empty.")

        except Exception as e:
            print(f"Warning: Could not load config from {key}: {e}")
            
        # Fallback to default paths if no specific config exists (secure mode)
        self.tls_config = {
            "CERT_PATH": str(tls_path),  # Path where the certificate file is located
            "KEY_FILE": str(Path("config/key.pem")),   # Path for RSA private key
            "SSL_CAPTCHA_ENABLED": True,             # Default to true if not explicitly disabled
        }

    def load_pre_shared_secrets(self):
        """Load pre-shared secrets from environment variables or config."""
        try:
            self.pre_shared_secrets = {key: value for key, value in Path("secrets").glob("*")}
            print(f"Loaded pre-shared secrets. Count: {len(self.pre_shared_secrets)}")
            
            if not all(s.exists() and s.stat().st_size > 0 for s in self.pre_shared_secrets.values()):
                raise RuntimeError(
                    "Pre-shared secrets must exist at least one file with content."
                )

        except Exception as e:
            print(f"Warning: Could not load pre-shared secrets. Using zero-key mode.")
            # Zero-key secure mode is enabled by default if no specific config exists, 
            # but we allow explicit disabling via environment variables for development.
            
    def get_tls_config(self) -> dict[str, str]:
        """Get the current TLS configuration dictionary."""
        return self.tls_config

    def setup_key_derivation(self):
        """Setup RSA key derivation from pre-shared secrets or env vars if not configured otherwise."""
        # Ensure we have at least one secret for DER generation
        all_secrets = set()
        
        try:
            for s in Path("secrets").glob("*"):
                if s.exists():
