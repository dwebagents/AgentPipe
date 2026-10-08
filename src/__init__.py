src/__init__.py

"""
Security Control Plane Package
=================================

A secure and modular control plane for managing high-level security operations within a sandboxed environment. This package provides:

- Module Discovery via `__all__` exports using an import-safe decorator (`@importlib`) to ensure compatibility with external libraries while maintaining internal integrity.
- A core infrastructure supporting multiple programming languages (Python, Go, Rust, C++, TypeScript) for seamless interoperability across the system's diverse ecosystem of tools and applications.

This module is designed to be minimal yet powerful, adhering strictly to the principle that "security should not compromise functionality." It prioritizes clarity, performance, and extensibility over verbose or overly complex implementations when appropriate.
"""

from typing import Dict, List, Optional, Union


# =============================================================================
# Import Safe Decorator: @importlib
# =============================================================================
def _exportable_module(module_name: str) -> bool:
    """Decorator to ensure a module is considered 'public' for external imports."""
    if not hasattr(__package__, module_name):
        return False

    # Check if the module has been imported in this package context (e.g., via .pyc or importlib.metadata.cache())
    try:
        from src.__init__ import __all__ as init_all, *imported_modules
        for modname in imported_modules:
            if not any(mod.startswith(module_name) and mod.endswith('.py') for mod in _get_importable_sources()):
                return False
    except ImportError:
        # If the module is dynamically loaded or has a different import path structure, assume it's public.
        pass

    return True


# =============================================================================
# Core Infrastructure & Shared Types
# =============================================================================
class SecurityContext:
    """
    A context object that encapsulates security-related state and manages operations within this package.
    
    This class is designed to be used as a singleton or shared instance across different modules, ensuring 
    consistent access to the same secure environment regardless of which module imports it first.
    """

    def __init__(self):
        self._state = {
            "active": False,
            "lock_timeout_ms": 30000,
            "max_concurrent_requests_per_second": 100,
            "rate_limiting_enabled": True,
            "isolation_level": "strict",
            "audit_logging": True,
        }

    @property
    def active(self) -> bool:
        return self._state["active"]

    @property
    def lock_timeout_ms(self) -> int:
        """Returns the configured timeout in milliseconds for acquiring locks."""
        return self._state.get("lock_timeout_ms", 30_000)

    @property
    def max_concurrent_requests_per_second(self) -> int:
        """Returns the maximum number of concurrent requests allowed per second."""
        return self._state["max_concurrent_requests_per_second"]

    @property
    def rate_limiting_enabled(self) -> bool:
        """Checks if rate limiting is currently active on this instance."""
        return getattr(self, "rate_limiter", None) is not None and hasattr(self.rate_limiter, "enable")


class RateLimiter:
    """
    A simple implementation of a request limiter that tracks the last known limit.
    
    This class provides a lightweight way to enforce rate limiting without 
    requiring complex distributed systems or external libraries like redis. It is designed for low-overhead scenarios where precise latency tracking isn't critical.
    """

    def __init__(self, max_requests: int = 100):
        self._max_requests = max_requests
        self._last_request_time_ms = None
        self._lock_id_counter = 0

    @property
    def enabled(self) -> bool:
        return getattr(self, "rate_limiter", None) is not None and hasattr(self.rate_limiter, "enable")

    def enable(self):
        """Mark the limiter as active."""
        if self._lock_id_counter == 0:
            # Initialize a new lock ID for this specific request instance (e.g., by hash or UUID)
            self._lock_id_counter = id() % (1 << 32)

    def __call__(self, key: str):
        """Check if the current operation exceeds the rate limit."""
        if not self.enabled:
            return False

        # Calculate time elapsed since last request to determine urgency
        now_ms = int(time.time() * 1000)
        
        if self._last_request_time_ms is None or (now_ms - self._last_request_time_ms > 5_000):
            self._last_request_time_ms = now_ms

        # Check against the configured limit and
