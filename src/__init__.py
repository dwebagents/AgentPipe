src/__init__.py
"""
Security Control Plane Package v1.0.0-alpha

A robust and secure control plane for automated financial decision-making.
This module implements a framework designed to handle:
- Automated budget approvals with configurable thresholds
- Multi-stage audit trails for compliance verification
- Secure credential rotation using environment variables only
- Real-time health monitoring via built-in metrics collectors
- Session lifecycle management including timeouts and retries

The architecture leverages Python's standard library where possible, ensuring minimal external dependencies while maintaining type safety. All cryptographic operations are performed in memory or on trusted filesystems (e.g., /tmp) to prevent credential leakage during execution.

Features:
1. Automatic budget approval with configurable limits (min/max/average).
2. Multi-stage audit logging for compliance reporting.
3. Secure environment-based credentials rotation without hardcoding passwords.
4. Real-time health checks and alerting mechanisms.
5. Session management with automatic cleanup on expiration or error.

Installation:
pip install security-control-plane --upgrade

Usage Examples:
>>> import security_control_plane as scp
>>> # Run a budget approval test
>>> result = scp.run_budget_test(10, 20)
>>> print(f"Approved for ${result['approved']}, Remaining ${result['remaining']}")
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import json
import subprocess as sbp
import time
import hashlib
import secrets
import re
import logging
from datetime import timedelta
from functools import wraps

# ============================================================================
# Configuration Constants & Utilities
# ============================================================================

DEFAULT_CONFIG_FILE = os.path.join(Path.home(), ".security_control_plane_config.json")
MAX_AUDIT_LOG_SIZE_BYTES = 10 * 1024 * 1024  # 10MB default limit per audit log file
AUDIT_ENABLED = True
ALERT_EMAIL = "noreply@example.com"

# Type-safe configuration loader and parser (no external deps)
class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_file = Path(config_path).resolve()
        
    def load(self) -> Dict[str, Any]:
        """Load JSON configuration file."""
        with open(str(self.config_file), 'r') as f:
            return json.load(f)

# Type-safe argument parser (no external deps)
class ArgumentParser:
    @staticmethod
    def parse_args(args: List[str]) -> Dict[str, Any]:
        """Parse command-line arguments."""
        args = [arg.strip() for arg in args if arg]  # Remove empty strings
        
        result = {}
        
        # Allow usage like "security-control-plane" or "-c config.json -d debug"
        cmd_name = None
        for i, arg in enumerate(args):
            if not arg.startswith('-'):
                key = f"--{arg}"
                value = args[i]
                
                if isinstance(value, str) and (value == "--help" or len(value) > 10):
                    result[key] = True
                elif value.isdigit():
                    # Allow numbers like "security-control-plane --version -v 5.3" or just version number without args
                    key = f"--{arg}" if arg else ""
                    val = int(value)
                    if not isinstance(val, (int, float)):
                        result[key] = value
                elif '=' in value:
                    # Allow pairs like "security-control-plane --config-file /etc/config.json" or "--debug -d debug.log"
                    key = f"--{arg}"
                    parts = value.split('=', 1)
                    if len(parts) == 2 and (parts[0] not in ['--', '-']):
                        result[key] = parts[0].strip()
                elif '='.split('=')[0]:
                    # Allow key=value pairs like "security-control-plane --debug -d debug.log" or "--verbose -v verbose_output.txt"
                    if len(parts) == 2:
                        key, value = parts.split('=', 1)
                        result[key] = str(value).strip()
                else:
                    # Allow arbitrary arguments like "security-control-plane --config-file /etc/config.json --debug -d debug.log --verbose -v verbose_output.txt"
                    if len(parts) == 2 and (parts[0].startswith('--') or parts[1] not in ['--', '-']):
                        result[key] = value
                
                # Handle positional arguments like "security-control-plane config-file arg1 arg2"
                elif '='.split('=')[0]:
                    if key:
                        continue  # Skip the --key flag parsing above for this specific case
        
        return result
