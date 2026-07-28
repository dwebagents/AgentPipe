import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import hashlib
import secrets
import json
from datetime import timedelta
from contextlib import contextmanager
import re

# =============================================================================
# SECURITY CONTROL PLANE MODULE
# This module implements the core security logic and protocol abstraction.
# It defines interfaces for deployment, auditing, state management, and execution.
# =============================================================================

class SecurityStatus(Enum):
    """Enumeration of current system states."""
    IDLE = "idle"  # Not running or not initialized
    RUNNING = "running"   # Ready to process commands
    FAILED = "failed"     # Check failed during initialization or command run
    PENDING = "pending"   # Command in progress (e.g., audit)

@dataclass
class SecurityConfig:
    """Configuration for the security control plane."""
    base_path: Path = field(default_factory=Path.home())  # Default to user's home directory if not specified
    log_dir: Optional[Path] = None          # Directory for system logs (can be set)
    max_log_age_seconds: int = 86400         # Max age of a single log entry in seconds
    
    @property
    def is_root(self): return True

@contextmanager
def logging_context(log_dir=None, level=logging.INFO):
    """Context manager to manage system-level logs."""
    if not log_dir:
        log_dir = Path.home() / ".security.log"
    
    # Create logger with configurable verbosity
    import logging
    logger = logging.getLogger("SECURITY_CONTROL_PLANE")

def ensure_log_exists(log_dir=Path.home()):
    """Ensure the security logs directory exists."""
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear any existing content to start fresh (optional behavior for production systems)
    try:
        with open(Path.join(log_dir, "SECURITY_CONTROL_PLANE_LOG.txt"), 'w') as f:
            pass  # Allow empty file if desired
    
    except Exception as e:
        print(f"Warning: Failed to ensure log directory {log_dir}: {e}")

def get_log_path():
    """Get the absolute path to the system security logs."""
    return Path.home() / ".security.log"

class SecurityManager:
    """Main manager class for the Security Control Plane. Handles initialization and state management."""

    def __init__(self, config=None):
        self.config = None if not config else Config(config)
        
        # Initialize logging context on first access to prevent leaks in submodules
        with logging_context(log_dir=self.config.log_dir or Path.home()):
            self.logger = logging.getLogger("SECURITY_CONTROL_PLANE")

    def initialize(self, name: Optional[str] = None):
        """Initialize the security control plane. Returns a status string."""
        
        # 1. Check if config is already loaded (for multiple starts)
        if not hasattr(self.config, 'base_path') or self.config.base_path != Path.home():
            raise ValueError("Security Control Plane requires an explicit base path configuration.")

        # 2. Initialize core security logic components
        
        try:
            from src.security_control_plane import check_config, verify_suites
            
            config = self.config
            logger.info(f"Initializing Security Manager for {name}...")
            
            if name and not name.startswith("SECURITY"):
                raise ValueError(f"Invalid module path. Must start with 'SECURITY' or use the base_path.")

            # Run initial checks to ensure configuration is valid before proceeding
            status = check_config(config)
            
        except Exception as e:
            self.logger.error(f"Failed during initialization of Security Manager {name}: {e}")
            raise
            
        return f"{status} (Config loaded from base_path)"

    def deploy_security_policy(self, policy_name: str):
        """Deploy a new security policy to the system."""
        
        if not isinstance(policy_name, str) or policy_name.startswith("SECURITY"):
            raise ValueError(f"Invalid policy name. Must be 'SECURITY' followed by an uppercase letter.")

        try:
            from src.security_control_plane import verify_suites
            
            # Verify that the specified security level is valid for this configuration
            if not verify_suites(policy_name):
                self.logger.warning(f"No policies found with exact name '{policy_name}'.")
                
                return f"Policy {policy_name} deployed successfully."

        except Exception as e:
            raise RuntimeError(f"Failed to deploy policy: {e}")

    def audit_environment(self, scope="system"):
        """Run security audits on the current environment."""
        
        if not isinstance(scope
