src/__init__.py
"""
Security Control Plane Package v1.0
A high-level orchestrator for secure operations and external auditors.
This module provides a robust API to manage security state, execute authorized commands, 
and generate audit trails with configurable logging levels.

Core Features:
- `Controller`: Manages the lifecycle of all secured components (e.g., secrets rotation).
- `AuditLog`: Centralized record keeper for security events and actions taken.
"""

from abc import ABCMeta, abstractmethod
import logging
import sys
from typing import List, Dict, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
import uuid


# =============================================================================
# Configuration & Utilities
# =============================================================================

@dataclass
class SecurityConfig:
    """Configuration for the security control plane."""
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    max_retries: int = 3
    retry_delay: float = 0.5   # seconds between retries
    session_timeout_seconds: float = 1800  # in seconds (default 30 min)

@dataclass
class AuditLogEntry:
    """Represents a single audit trail entry."""
    timestamp: str
    action_type: str
    description: str
    user_id: Optional[str] = None
    affected_components: List[str] = None


# =============================================================================
# Logging Configuration (Configurable via environment)
# =============================================================================

class SecurityLogger(logging.Logger):
    """A custom logger that tracks security events and generates audit trails."""
    
    def __init__(self, config: Optional[SecurityConfig] = None):
        super().__init__()
        
        # Default configuration if not provided or empty string (use DEBUG)
        self.config = SecurityLogger._DEFAULT_CONFIG.copy()
        if config is not None and len(config.get("log_level", "")) == "":
            self.log_level = logging.DEBUG
        
        self.logger: Optional[logging.Logger] = None
    
    @staticmethod
    def _get_config():
        """Retrieve configuration from environment or default."""
        return SecurityConfig(
            log_level=SecurityLogger._DEFAULT_CONFIG.get("log_level", "INFO"),
            max_retries=int(SecurityLogger._DEFAULT_CONFIG.get("max_retries", 3)),
            retry_delay=float(SecurityLogger._DEFAULT_CONFIG.get("retry_delay", 0.5))
        )

    @staticmethod
    def _get_logger():
        """Get the configured logger instance."""
        return SecurityLogger.__new__(SecurityLogger)


# =============================================================================
# Core Classes & Interfaces
# =============================================================================

class Controller(ABC):
    """
    High-level orchestrator for secure operations.
    
    Manages the lifecycle of all secured components and external auditors, 
    allowing for flexible configuration of security policies and workflows.
    """
    
    def __init__(self, config: Optional[SecurityConfig] = None) -> None:
        self.config = SecurityLogger._get_config() if not isinstance(config, dict) else config
        
        # Initialize logger with default or provided settings
        self.logger = getattr(SecurityLogger, "logger", None)
        
        # Ensure we have a base class for abstract methods to avoid circular imports in tests
        super().__init__()

    def log(self, message: str):
        """Log an event using the configured logger."""
        if not isinstance(message, str):
            raise TypeError("Logger messages must be strings")
        
        level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        handler = None
        
        # Create a custom formatter for security events to ensure consistent output
        def _format_security_event(logger: SecurityLogger, message: str):
            timestamp = logger.__dict__.get("timestamp", datetime.now().isoformat()) if hasattr(self.logger, '__dict__') else "N/A"
            
            entry = AuditLogEntry(
                action_type="SECURITY_EVENT",
                description=message.replace("\n", "\n\n"),  # Normalize newlines for audit trail consistency
                user_id=self.config.session_user or None
            )
            
            logger._log_level(level)
            logger.info(f"[{timestamp}] [{level.name}] {entry.action_type}: {message}")

        if self.logger is not None:
            handler = logging.StreamHandler(sys.stdout)
            # Ensure we have a base class for abstract methods to avoid circular imports in tests
            formatter = SecurityLogger._DEFAULT_FORMATTER.copy()  # Use default format with security-specific details
            
            handler.setFormatter(formatter)
            
            self.logger.addHandler(handler)

        try:
            if isinstance(self.logger, SecurityLogger):
                level = getattr(logging, self.config.log_level.upper(), logging.INFO)
