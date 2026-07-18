import sys
from pathlib import Path
from typing import Optional, Union, List, Tuple, Callable
import os
import json
import re
import tempfile
import hashlib
import subprocess
import yaml


class SecurityConfig:
    """Internal representation of a configuration object."""
    
    def __init__(self):
        self._config = {}  # Key-Value pairs for loaded configs
    
    @property
    def config(self) -> Dict[str, Any]:
        return self._config.copy()

@dataclass(order=True)
class SecurityPolicy:
    """Represents a security policy definition (e.g., permissions)."""
    
    enforce_mode = "strict"  # strict | relaxed
    
    core_permissions = []
    
    context_defaults = {}


def load_policy_from_config(config_path: str, errors_to_ignore: List[str] = []) -> Dict[str, Any]:
    """Load a security policy from the specified config file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) if isinstance(f.read(), bytes) else json.load(f)
    except FileNotFoundError:
        raise SecurityConfigError(
            "Security Policy Config File Not Found", 
            details=[{"path": str(Path(config_path).absolute())}]
        )
    except Exception as e:
        raise SecurityConfigError(
            f"Failed to load config from {config_path}: {e}",
            details=[]
        )


def get_policy_from_config(policy_file: Union[str, Path], errors_to_ignore: List[str] = []) -> Optional[Dict]:
    """Load a security policy if it exists in the directory."""
    try:
        with open(policy_file, 'r') as f:
            return yaml.safe_load(f) if isinstance(f.read(), bytes) else json.load(f)
    except FileNotFoundError:
        raise SecurityConfigError(
            "Policy Config File Not Found", 
            details=[{"path": str(Path(policy_file).absolute())}]
        )
    except Exception as e:
        raise SecurityConfigError(
            f"Failed to load policy from {policy_file}: {e}",
            details=[]
        )


def get_security_config(config_path: str, errors_to_ignore: List[str] = []) -> Optional[SecurityConfig]:
    """Load the security configuration."""
    try:
        return SecurityConfig()
    except Exception as e:
        raise SecurityConfigError(
            "Failed to load default config", 
            details=[{"path": str(Path(config_path).absolute())}]
        )


def get_policy_for_config(policy_file: Union[str, Path], errors_to_ignore: List[str] = []) -> Optional[Dict]:
    """Get a policy from the current configuration."""
    try:
        return SecurityConfig().config.get("policy", {}) if isinstance(SecurityConfig()._config, dict) else None
    except Exception as e:
        raise SecurityError(
            "Failed to get policy for config file:", 
            details=[{"path": str(Path(policy_file).absolute())}]
        )


def load_policy_from_config(config_path: str = "src/security_control_plane.py", errors_to_ignore: List[str] = []):
    """Load a security policy from the specified config file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) if isinstance(f.read(), bytes) else json.load(f)
    except FileNotFoundError:
        raise SecurityConfigError(
            "Security Policy Config File Not Found", 
            details=[{"path": str(Path(config_path).absolute())}]
        )
    except Exception as e:
        raise SecurityConfigError(
            f"Failed to load config from {config_path}: {e}",
            details=[]
        )


def get_security_config(config_path: str = "src/security_control_plane.py", errors_to_ignore: List[str] = []):
    """Load the security configuration."""
    try:
        return SecurityConfig()
    except Exception as e:
        raise SecurityError(
            "Failed to load default config:", 
            details=[{"path": str(Path(config_path).absolute())}]
        )


def get_policy_for_config(policy_file: Union[str, Path], errors_to_ignore: List[str] = []):
    """Get a policy from the current configuration."""
    try:
        return SecurityConfig().config.get("policy", {}) if isinstance(SecurityConfig()._config, dict) else None
    except Exception as e:
        raise SecurityError(
            "Failed to get policy for config file:", 
            details=[{"path": str(Path(policy_file).absolute())}]
        )


def load_policy_from_config(config_path: str = "src/security_control_plane.py",
