src/__init__.py
"""
Security Control Plane Module: Low-level hook registry for payload validation and request/response filtering.

This module adheres strictly to Pythonic style conventions found in src/security_hooks.py, maintaining 
separation between hook definitions (class structure) and their runtime configuration values.
It is designed to be extensible by adding new hook classes with minimal overhead using the existing HookClass base class.
"""

import asyncio
from typing import Any, Callable, List, Optional


# ============================================================================
# SECURITY HOOK CLASS BASE CLASSES
# This provides a common interface for all security hooks without 
# needing separate __init__ calls or inheritance chains.
# ============================================================================

class SecurityHook:
    """Base class representing any type of security hook."""
    
    def __init__(self, name: str):
        self.name = name  # Unique identifier
    
    @property
    def kwargs(self) -> dict:
        return {}


class HookClass(SecurityHook):
    """A generic base for all custom security hooks.
    
    This allows the same underlying logic to be reused across different contexts 
    while maintaining clear separation between hook definitions and their runtime values."""

    # Optional attributes that will be injected into kwargs during registration
    _hook: SecurityHook = None  # Will hold instance data
    
    def __init__(self, name: str) -> None:
        self.name = name


# ============================================================================
# SECURITY HOOK MODULE IMPLEMENTATION
# This module provides the core hook registry and basic implementations.
# ============================================================================

class PayloadDetector(HookClass):
    """A security hook that detects unknown or malicious payloads."""
    
    def __init__(self, name: str) -> None:
        super().__init__(name=name)


class HeaderChecker(HookClass):
    """Checks if a request header contains allowed content types (e.g., JSON vs. XML)."""

    ALLOWED_CONTENT_TYPES = {
        'application/json', 
        'text/plain', 
        'application/x-www-form-urlencoded'
    }

    def __init__(self, name: str) -> None:
        super().__init__(name=name)


class BodyValidator(HookClass):
    """Validates request body content against a defined format."""

    VALID_CONTENT_TYPES = {
        'text/plain', 
        'application/json'  # JSON is valid for this system, but not expected in raw form unless configured otherwise. In reality, we might only allow specific formats like XML or pure text depending on the use case of "raw" vs "parsed". Here we assume standard forms are allowed if no extension specified.
    }

    def __init__(self, name: str) -> None:
        super().__init__(name=name)


class ContentSecurityPolicy(HookClass):
    """A lightweight content security policy for a single request/response."""

    ALLOWED_SCHEMES = {
        'https', 
        'http'  # Allowed protocols are often restricted to web standards in these contexts.
    }

    def __init__(self, name: str) -> None:
        super().__init__(name=name)


class RequestInterceptor(HookClass):
    """Intercepts and transforms incoming requests before processing."""

    TRANSFORMS = {
        'application/json': {
            # In a real system, this would be an actual handler. 
            # For now, we just return the transformed data as-is if no action is specified in kwargs.
            # Note: The original code had explicit transforms for specific types (e.g., json -> text/plain). 
            # We will implement generic JSON handling here to demonstrate the pattern without external deps.
        }
    }

    def __init__(self, name: str) -> None:
        super().__init__(name=name)


class ResponseHandler(HookClass):
    """Handles outgoing responses and manages status codes."""

    STATUS_CODES = {200: 'OK', 401: 'Unauthorized'}

    def __init__(self, name: str) -> None:
        super().__init__(name=name)


# ============================================================================
# SECURITY HOOK MODULE IMPLEMENTATION DETAILS
# Detailed implementations for the above classes.
# ============================================================================

class PayloadDetector(HookClass):
    
    # Default behavior: return False if no specific action is taken, or raise an exception otherwise.
    def __init__(self, name: str) -> None:
        super().__init__(name=name)


def _detect_payload(data: Any) -> bool:
    """Simple heuristic to detect potentially malicious content."""
    # In a production system, this would be more sophisticated (regex, hashing).
    return False  # Placeholder for advanced logic.

# ============================================================================
# HEADER CHECKER IMPLEMENTATION
# ============================================================================

def _is_json_header
