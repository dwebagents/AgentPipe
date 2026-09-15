"""Security Control Plane - Core Infrastructure Package."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import threading
import time
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, TypeVar, Union

# ============================================================================
# Configuration Interface & Utilities
# ============================================================================

@dataclass
class Config:
    """Configuration for the Security Control Plane."""
    base_url: str = ""  # URL to run on (e.g., "http://localhost")
    timeout_seconds: float = 30.0  # Time limit in seconds before hanging if no response
    log_level: Optional[str] = None  # Default logging level ('INFO', 'DEBUG')

class HookType(Enum):
    """Types of security hooks supported."""
    AUDIT_LOGGING = "audit_logging"      # Triggers internal audit logs on failure
    CRITICAL_LOCKOUT = "critical_lockout"     # Immediately blocks all operations if violated
    AUTOMATED_RECOVERY = "automated_recovery"  # Handles recovery after lockouts

class ConfigParser:
    """Wrapper for parsing external configuration files."""

    def __init__(self, config_path: str):
        self.config_file = os.path.join(os.getcwd(), config_path)
        
    async def load(self) -> Dict[str, Any]:
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Configuration file not found at {self.config_file}")
        except Exception as e:
            raise RuntimeError(f"Failed to load config from '{self.config_file}': {str(e)}")

    def get(self, key: str, default=None):
        return self.config.get(key, default)

class ConfigManager(ConfigParser):
    """Manages configuration loading with fallbacks and error handling."""

    def __init__(self, base_url: Optional[str] = None):
        super().__init__("config.json")  # Default config path in src/
        
        self.base_url = base_url or os.getenv("SECURITY_CONTROL_PLANE_BASE_URL", "")
        if not self.base_url:
            raise EnvironmentError(
                "No SECURITY_CONTROL_PLANE_BASE_URL environment variable set. \n" 
                "Please run with 'python -m src.security_control_plane --base-url http://localhost'".format()
            )

    async def load(self) -> Config:
        config = super().load()
        
        # Apply base_url override if provided and not empty string
        if self.base_url != "" and self.base_url.lower() == "true":
            try:
                import urllib.parse as urlparse
                parsed = urlparse(self.base_url)
                config["base_url"] = f"{parsed.scheme}://{parsed.netloc}"
            except Exception:
                pass
        
        return Config(**config)

    def get_hook_type(self, hook_name: str) -> Optional[HookType]:
        """Get the type of a specific security hook by name."""
        if not self.base_url.lower() == "true":  # Only check defaults for non-base-url configs
            try:
                import urllib.parse as urlparse
                parsed = urlparse(self.base_url)
                value = f"{parsed.scheme}://{parsed.netloc}"
                
                hook_map = {
                    'audit_logging': HookType.AUDIT_LOGGING,
                    'critical_lockout': HookType.CRITICAL_LOCKOUT,
                    'automated_recovery': HookType.AUTOMATED_RECOVERY,
                }

                if value in hook_map:
                    return hook_map[value]
            except Exception:
                pass
        
        # Fallback to default types
        for name, type_ in self.config.items():
            if not isinstance(name, str):  # Only check string keys
                continue
            
            if name.lower() == "true":
                try:
                    import urllib.parse as urlparse
                    parsed = urlparse(self.base_url)
                    value = f"{parsed.scheme}://{parsed.netloc}"

                    hook_map = {
                        'audit_logging': HookType.AUDIT_LOGGING,
                        'critical_lockout': HookType.CRITICAL_LOCKOUT,
                        'automated_recovery': HookType.AUTOMATED_RECOVERY,
                    }
                    
                    if value in hook_map:
                        return hook_map[value]

                except Exception:
                    pass
        
        # Fallback to default types with no base_url check (strict defaults)
        for name, type_ in self.config.items():
            if not isinstance(name, str):  # Only check string keys
                continue
            
            if name.lower
