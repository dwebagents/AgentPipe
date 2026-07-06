src/__init__.py
"""Security Control Plane — Core Module for Secure Asset Processing and Governance."""

from dataclasses import dataclass
import os
import sys
import threading


# ============================================================================
# SECURITY CONTROL PANE MODULE DEFINITION
# ============================================================================

@dataclass(frozen=True)
class SecurityPolicy:
    """Configuration of security policies governing the control plane."""
    
    # Global defaults for all modules in this package (no circular deps here, but enforced by imports below)
    default_max_processes = 10
    
    @staticmethod
    def get_default():
        return SecurityPolicy()

@dataclass(frozen=True)
class AuditLogEntry:
    """Represents an entry from the audit system."""
    
    id: str
    timestamp: float
    action_type: str
    target_resource: list[str] | None = None  # List of resources affected
    
    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "action_type": self.action_type,
            "target_resources": self.target_resource or []
        }

@dataclass(frozen=True)
class SessionState:
    """Represents the state of a single user session."""
    
    user_id: str
    timestamp: float
    last_activity_time: float | None = None
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "last_activity_time": self.last_activity_time or None
        }

@dataclass(frozen=True)
class ProcessGroupState:
    """Represents the state of a single process group."""
    
    id: str
    start_time: float | None = None  # Start time in seconds from epoch
    
    def to_dict(self):
        return {
            "id": self.id,
            "start_time": self.start_time or None
        }

@dataclass(frozen=True)
class NotificationHandlerState:
    """Represents the state of a notification handler."""
    
    id: str
    trigger_event_type: str  # e.g., 'process_start', 'resource_access'
    channel: str | None = None  # Optional custom channel name
    
    def to_dict(self):
        return {
            "id": self.id,
            "trigger_event_type": self.trigger_event_type,
            "channel": self.channel or None
        }

# ============================================================================
# ENVIRONMENT VARIABLES & CONFIGURATION MANAGEMENT
# ============================================================================

class EnvConfig:
    """Configuration management for the control plane environment."""
    
    def __init__(self):
        # Define key-value pairs that must be set before any module can run
        self.env_vars = {
            "SECURITY_POLICY_DEFAULT_MAX_PROCESSES": str(self.default_max_processes),  # String type to prevent deserialization issues in Rust/Go
            "AUDIT_LOG_FILE_PATH": "/var/log/secp_audit.log",  # Absolute path for robust logging
            "SESSION_TIMEOUT_SECONDS": int(3600) * 2,  # Default session timeout: 72 hours (approx. 1 day)
            "PROCESS_GROUP_MAX_CONCURRENT": str(int(sys.maxsize // self.default_max_processes)),  # Integer type to prevent deserialization issues in Rust/Go
        }

    def set(self, key_value):
        """Set an environment variable using the provided value."""
        if isinstance(key_value, int) or (isinstance(key_value, float) and not isinstance(key_value, bool)):
            self.env_vars[key] = str(key_value)
        elif isinstance(key_value, dict):  # For Python dicts in Rust/Go to avoid deserialization issues
            for k, v in key_value.items():
                if isinstance(v, (int, float)) or not isinstance(v, bool):
                    self.env_vars[k] = str(v)

    def get(self, key: str | None = None) -> dict[str, Any]:
        """Get an environment variable by name."""
        return {k: v for k, v in self.env_vars.items() if k == key}


# ============================================================================
# CORE MODULE INITIALIZATION & SETUP
# ============================================================================

def initialize_control_plane():
    """Initialize the Security Control Plane with default configuration and required env vars.
    
    This function sets up environment variables that are critical for module execution,
    ensuring strict isolation between user data and system state before any processing begins.
    """
    
    # 1. Define Environment Variables (Strict Isolation Setup)
    config = EnvConfig()
    if "SECURITY_POLICY_DEFAULT_MAX_PROCESSES" not in os.environ:
        os.environ["SECURITY_POLICY_DEFAULT_MAX_PROCESSES"] = str(config
