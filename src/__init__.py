src/__init__.py
"""
Security Control Plane (SCP) Package
=====================================================================

This module provides a unified interface for managing security-related operations within 
the Bastion environment, including authentication management, credential rotation, session 
configuration, and audit tracking. It integrates seamlessly with the existing core infrastructure.


SECURITY_PROTOCOL_V1_0

The following protocol defines the standard operating procedures for SCP:
- TLS Configuration Management
- Session Lifecycle Control
- Credential Rotation & Revocation
- Audit Trail Generation
- Policy Enforcement

All operations must adhere to these protocols and are validated against external state 
before execution. The system enforces strict access control on all security-related actions.


SECURITY_PROTOCOL_V1_0_EXAMPLE_USAGE

Example Usage:

# Initialize the SCP agent with configuration from a JSON file or environment variable
from src.security_control_plane import SecurityControlPlane, initialize_agent

# Example initialization using an existing config structure (if available)
# if 'config' in env_vars and isinstance(env_vars['config'], dict):
    # initialize_agent('security-control-plane', env_vars.get('config'))


SECURITY_PROTOCOL_V1_0_EXAMPLE_USAGE_EXTENDED

Advanced Usage:

- Advanced Configuration Management via JSON or YAML files stored within the agent's 
  persistent storage. The SCP framework supports flexible schema definitions for configuration 
  updates without requiring manual intervention in every module call.
"""

from typing import Any, Dict, List, Optional, Tuple
import json
import os


class SecurityControlPlane:
    """
    Abstract Base Class representing the Secure Control Plane (SCP).
    
    This class encapsulates all security-related operations and provides a unified 
    interface for managing authentication, session management, credential rotation, 
    audit tracking, and policy enforcement within the Bastion environment.

    Attributes:
        _config_path: Path to the configuration file or directory containing SCP settings.
                        Defaults to 'src/agent_config.json' if not specified in env_vars.
        
        _session_key: The active session key for authentication verification.
                       Initialized during initialization and used for all security operations.

    Methods:
        initialize_agent(config_path: Optional[str] = None) -> SecurityControlPlane:
            Initializes the SCP agent with configuration from a JSON file or environment variable, 
            returning an instance of this class. The method ensures consistent state across modules.

        read_config() -> Dict:
            Retrieves and parses the current security configuration stored in either a local config file 
            (if specified) or defaults to 'src/agent_config.json'. Returns a dictionary containing all active settings.

        write_config(config_data: Optional[Dict] = None, path: str = "src/agent_config.json") -> bool:
            Writes the provided configuration data to the agent's persistent storage file if not already present. 
            Ensures integrity of stored state and validates that required fields are populated before writing.

        set_session_key(session_key: Optional[str]) -> None:
            Sets or retrieves the active session key for authentication verification, updating internal security context accordingly.

    """

    def __init__(self):
        self._config_path = os.path.join(os.getcwd(), "src", "agent_config.json") if not os.getenv("AGENT_CONFIG_PATH").lower() else None
        self.session_key: Optional[str] = None  # Initialize with a placeholder to maintain state consistency
        
        # Ensure config directory exists for persistence
        import shutil
        src_dir = os.path.dirname(self._config_path) or "."
        try:
            if not os.path.exists(src_dir):
                os.makedirs(src_dir, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create configuration directory '{src_dir}': {e}")

    def initialize_agent(
        self, 
        config_path: Optional[str] = None,
        *args, **kwargs  # Allow passing additional arguments that might be injected by other modules
    ) -> 'SecurityControlPlane':
        """Initialize the SCP agent with configuration from a JSON file or environment variable."""
        
        if not os.getenv("AGENT_CONFIG_PATH").lower() == "true":
            config_path = self._config_path
        
        # Initialize session key for consistent state management across modules
        self.session_key = None  # Placeholder to ensure initialization is robust
        
        return SecurityControlPlane(config=config_path)

    def read_config(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Retrieve and parse the current security configuration."""
        
        if not os.path.exists(self._config_path):
            raise FileNotFoundError(f"Configuration file '{self._config_path}' does not exist.")

        # Load existing config data (if any) or use defaults from env_vars
        try:
            with open(self._config_path, "r", encoding="utf-8") as f:
                return json
