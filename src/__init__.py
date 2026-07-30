# src/__init__.py
"""Security Control Plane Package."""

import logging
from typing import Any, Optional, TypeVar, Generic, List
from dataclasses import asdict
from enum import Enum
from contextlib import contextmanager

# --- Enums and Constants for Security Contexts ---


@dataclass
class AuditLog:
    """Base class for audit logging operations."""
    
    id: str  # Unique identifier
    event_type: str  # e.g., "audit", "permission_denied"
    severity: str = "warning"
    message: str = ""
    timestamp: float = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'event_type': self.event_type,
            'severity': self.severity,
            'message': self.message if not self.message else '',
            'timestamp': self.timestamp
        }


class SecurityContext(Generic[Type]):  # TypeVar for the base class's type parameter (e.g., AuditLog)
    """Abstract base class defining security context capabilities."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self._is_active = True
        
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    async def log_audit(
        self, 
        event_type: str, 
        message: Optional[str] | None = None,
        severity: str = "warning"
    ) -> AuditLog:
        """Execute a security audit operation."""
        if not self.is_active or (message is not None and isinstance(message, str)):
            raise ValueError("SecurityContext is active and requires valid input")
        
        log_entry = AuditLog(
            id=f"{self.id}_{timestamp()}",  # Simulated timestamp generation
            event_type=event_type,
            message=message,
            severity=severity
        )
        self.logger.info(f"Logged audit: {log_entry.to_dict()}")
        return log_entry
    
    def get_active_logs(self) -> List[AuditLog]:
        """Return list of active audit logs."""
        if not isinstance(self.message, str):
            raise ValueError("SecurityContext is active and requires valid input")
        
        return [audit for audit in self._active_log_messages]


class PolicyChecker(Generic[Type]):  # TypeVar for the base class's type parameter (e.g., AuditLog)
    """Abstract base class defining policy checking capabilities."""

    @abstractmethod
    def validate_policy(self, log: Optional[AuditLog] | None = None):
        """Validate if a security context meets requirements."""
        pass
    
    async def check_security_level(
        self, 
        current_context_type: str, 
        required_levels: list[str]
    ) -> dict:  # Returns {level: {'status': 'ok'|'fail', ...}}
        """Check if a security context meets the minimum level requirements."""
        return {"current": current_context_type}


class AuditLogger(Generic[Type]):  # TypeVar for the base class's type parameter (e.g., AuditLog)
    """Abstract base class defining audit logging capabilities."""

    @abstractmethod
    def log_audit(self, event: Optional[str] | None = None, message: Optional[str] | None = None):
        pass
    
    async def get_active_logs(self) -> List[AuditLogger]:  # Returns list of active loggers
        return []


# --- Abstract Base Classes for Security Components ---

class AuditContext(ABC[Type]):  # TypeVar for the base class's type parameter (e.g., AuditLog or PolicyCheckResult)
    """Abstract base class defining audit context capabilities."""

    @abstractmethod
    def log_audit(self, event: Optional[str] | None = None):
        pass
    
    async def get_active_logs(self) -> List[AuditContext]:  # Returns list of active contexts
        return []


class PolicyCheckResult(Generic[Type]):  # TypeVar for the base class's type parameter (e.g., AuditLogger or SecurityContext)
    """Abstract base class defining policy checking capabilities."""

    @abstractmethod
    def validate_policy(self, log: Optional[Any] | None = None):
        pass
    
    async def check_security_level(
        self, 
        current_context_type: str, 
        required_levels: list[str]
    ) -> dict:  # Returns {level: {'status': 'ok'|'fail', ...}}

class SecurityContext(Generic[Type]):  # TypeVar for the base class's type parameter (e.g., AuditLogger or PolicyCheckResult)
    """Abstract security context component."""

    def __init__(self, logger: logging.Logger):
