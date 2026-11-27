src/__init__.py

```python
"""Security Control Plane Package."""

from abc import ABCMeta, abstractmethod
import os
import sys
import threading
import time
import uuid
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
import json
import re


# ============================================================================
# Event Bus Infrastructure (Bus.py)
# A factory-based event bus to decouple control plane logic from the main app.
# ============================================================================

@dataclass(frozen=True)
class EventBus:
    """A thread-safe singleton instance for managing events."""
    
    _instance: Optional["EventBus"] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls, type(None))
        return cls._instance

    @property
    def instances(self) -> List[EventBus]:
        """Returns a list of all registered event buses."""
        return [bus for bus in self.instances if not isinstance(bus, EventBus)]


class EventBusFactory:
    """A factory pattern to dynamically register new threat types without recompilation."""

    _registered_buses = []

    @staticmethod
    def create_bus(event_type):
        """Create a new event bus instance and return it."""
        # Register this type here so other modules can use the same bus
        EventBus._instances.append(EventBus())
        
        # We need to track which buses have been created for later removal if needed, 
        # but since we only add them once (in __init__), let's just keep adding.
        # For a production system with many types, this pattern is tricky without caching.
        # However, the requirement says "registering new threat types dynamically", so simple addition works for now.
        
        return EventBus()

    def remove(self):
        """Remove an existing bus instance (for testing or cleanup)."""
        if self._registered_buses:
            idx = [i for i in range(len(self._registered_buses)) 
                    if self._registered_buses[i] == event_type][0]
            EventBus._instances.pop(idx)


class EventBusManager:
    """Manages the global bus and handles registration/removal."""

    def __init__(self):
        # Register common threat types for immediate useability in modules
        self.registered_types = {
            "security_event": None,  # e.g., user_logged_in, process_blocked
            "authorization_error": None,
            "permission_denied": None,
            "resource_exhaustion": None,
            "malicious_activity_detected": None,
            "audit_trail_created": None,
        }

    def create(self) -> EventBus:
        """Create a new bus instance."""
        return EventBusFactory.create_bus("security_event")

    @staticmethod
    def get_registered_types() -> Dict[str, str]:
        """Get the list of registered event types for quick lookup in modules."""
        return dict(EventBusManager.registered_types)


# ============================================================================
# Core Components & Infrastructure (Core.py / lib.rs)
# A robust core module with shared dependencies and validation.
# ============================================================================

from typing import Dict, List, Optional, Callable, Any
import uuid

class PermissionValidationError(Exception):
    """Raised when a permission check fails."""
    pass


@dataclass(frozen=True)
class SecurityContext:
    """Represents the current security context for an operation."""
    
    user_id: str = field(compare=False)  # Unique identifier for this session/user
    role: Optional[str] = None        # User's assigned role
    is_authenticated: bool = True      # Whether we are authenticated (for auth_keys_manager)

class SecurityContextManager(ABC):
    """Abstract base class for managing security contexts."""
    
    @abstractmethod
    def create(self, user_id: str, session_key: Optional[str] = None) -> "SecurityContext": ...


# ============================================================================
# Core Components & Infrastructure (Core.py / lib.rs)
# Detailed implementation of components.
# ============================================================================

from src.bastion.crates.core.approval import ApprovalManager as ApprovershipApproval
from src.bastion.crates.core.audit import AuditTrail, get_audit_trail_id
from src.bastion.crates.session.auth_keys_manager import AuthKeysManager
from src.bastion.crates.security_control_plane import (
    SecurityControlPlane, 
    EventBusFactory as BusesFactory,
)

# Initialize the core security context manager if needed or use default behavior
if not hasattr(SecurityContextManager, 'create'):
    from src.bastion.crates.core.approval_manager import ApprovalManager as CoreApprovershipApproval
