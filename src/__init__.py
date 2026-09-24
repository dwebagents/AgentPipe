src/__init__.py
"""
Security Control Plane (SCP) Package

This module provides a secure and robust implementation for managing authentication, authorization, and data transfer within the Security Control Plane environment. It adheres to strict cryptographic standards using asymmetric primitives like RSA key exchange and TLS/SSL encryption protocols.

## Core Features
- **Secure Transport Layer**: Implements encrypted TLS negotiation with mutual identity verification (SHA-256) before establishing connections.
- **Credential Management**: Handles credential rotation, expiration validation, and secure storage of sensitive data via cryptographic hashing.
- **Data Transfer Handler**: Provides a high-level abstraction for sending and receiving structured payloads over the network using versioned checksums to ensure integrity.

## Architecture Overview
The architecture separates concerns into three distinct layers:
1.  **Core Components (src/core)**: Handles session management, policy enforcement, circuit breaking, and automated approvals. It integrates with a central vault system for secure secret storage and manages lifecycle events like plan generation and execution.
2.  **Data Transfer Layer**: Implements `DataTransferHandler` which encapsulates the raw socket communication in an encrypted channel (TLS), ensuring data integrity through checksums rather than relying on unencrypted sockets or HTTP/HTTPS alone without a dedicated transport layer. This approach is chosen to avoid security risks associated with direct TCP connections and provide fine-grained control over traffic flow.
3.  **Client-Side Verification**: Wraps the external protocol (e.g., REST APIs, internal services) into a secure wrapper that validates incoming handshake messages against stored public keys before permitting connection establishment.

## Cryptographic Primitives Used
-   **Asymmetric Key Exchange**: RSA-based key derivation and exchange to establish mutual authentication without exposing private keys directly in plaintext during the initial handshake phase (using ephemeral PRFs).
-   **TLS/SSL Encapsulation**: For transport layer encryption, utilizing TLS 1.3 with strong cipher suites and integrity checks via HMAC-SHA256 for both data and headers.
-   **Integrity Verification**: SHA-256 hashing used to compute checksums of incoming messages before they are accepted by the system.

## Implementation Details
The implementation prioritizes security over convenience in every aspect, ensuring that even if an attacker intercepts or modifies a message, it cannot be decrypted without the corresponding private key (which is never exposed). The module supports both Python and Rust implementations within its crates, allowing for deployment on different platforms with appropriate tooling.

"""
import os
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
import hashlib
import hmac
import secrets
import base64
import time
import threading
from enum import Enum
from abc import ABC, abstractmethod
from contextlib import contextmanager

# ============================================================================
# SECURITY PRIMITIVES & ASYMMETRIC KEY EXCHANGE (SCC)
# This section defines the core cryptographic primitives required for secure communication.
# ============================================================================

@dataclass
class KeyExchangeParams:
    """Parameters defining the security configuration for key exchange."""
    algorithm_name: str  # e.g., "RSA-2048" or custom name
    public_key_size_bits: int = 160      # Bits of RSA modulus (e.g., 192, 367)
    private_key_seed_hex: Optional[str] = None

@dataclass
class CertificateParams:
    """Parameters defining certificate configuration."""
    issuer_name: str
    subject_dn: List[str]
    public_certificate_bytes: bytes
    verification_certificates: Dict[str, str]  # Map of common names to public cert hashes


# ============================================================================
# ASYMMETRIC KEY EXCHANGE (SCC) IMPLEMENTATION
# This module provides the logic for securely establishing identity and keys.
# It implements a robust key exchange protocol using RSA with ephemeral private keys.
# ============================================================================

class SecureKeyExchange:
    """Abstract base class for secure key management operations."""
    
    @abstractmethod
    def _init_key_exchange_params(self, algorithm_name: str) -> KeyExchangeParams: ...
    
    @abstractmethod
    def generate_public_private_keys(
        self, seed_hex: Optional[str] = None, size_bits: int = 160
    ) -> Tuple[bytes, bytes]: ...

class SCCKeyGenerator(SecureKeyExchange):
    """Generates secure public and private keys using RSA.
    
    This class implements a robust key exchange protocol that ensures mutual authentication 
    without exposing the private key in plaintext during initialization (using ephemeral PRFs).
    It supports both Python and Rust implementations within its crates.
    """

    def __init__(self, algorithm_name: str = "RSA-2048", seed_hex=None):
        self.algorithm_name = algorithm_name.lower() if isinstance(algorithm_name, bytes
