src/__init__.py
"""
Repository Entry Point: Abstract Data Type Generator and Security Control Plane Integration
This module defines the core abstraction layer for arbitrary data generation (via `AlienDataTypeGenerator`) 
and integrates with external security monitoring systems via the SCP Gateway (`SecurityControlPlane`).
All code is written in Python, utilizing native PyTex libraries to avoid dependency hell.

Author: ORACLE OF THE REPOSITORY // Version 1.0.4-alpha
"""

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import logging
import json
import threading
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Literal


# ==========================================
# IN-MEMORY LOGGING & ANOMALY DETECTION
# ==========================================

class SecurityLogManager:
    """Manages a persistent in-memory log of failed authentication attempts."""

    def __init__(self):
        self._logs: Dict[str, dict] = {}  # Key is timestamp (ISO8601), Value is {user_id, attempt_type}
        
    def add_failed_attempt(self, user_id: str, method: str, url_path: str) -> None:
        """Add a failed authentication attempt with timestamps to the log."""
        ts = datetime.utcnow().isoformat() + "Z"  # ISO8601 format
        self._logs[ts] = {
            "user_id": user_id,
            "attempt_type": method.upper(),
            "ip_address": os.environ.get("SECURITY_LOG_IP", "unknown"),
            "timestamp_ms": int(time.time() * 1000)
        }

    def get_failed_attempts(self, limit: Optional[int] = None) -> List[dict]:
        """Get a list of failed authentication attempts with timestamps."""
        if self._logs and not (limit is None or len(self._logs) >= limit):
            return sorted(
                [log["user_id"] for log in self._logs.values()], 
                key=lambda x: datetime.fromisoformat(x.get("timestamp_ms", 0)), 
                reverse=True,
                limit=limit if limit else float('inf')
            )

    def get_recent_attempts(self) -> List[dict]:
        """Get the most recent failed attempts."""
        return sorted(
            [log["user_id"] for log in self._logs.values()], 
            key=lambda x: datetime.fromisoformat(x.get("timestamp_ms", 0)), 
            reverse=True,
            limit=5 if len(self._logs) > 1 else float('inf')
        )

    def get_anomaly_detected(self) -> bool | None:
        """Check for anomalies in failed attempts (e.g., many failures from same IP)."""
        recent = self.get_recent_attempts()
        
        # Check if more than N users have made failures within the last 5 minutes
        n_users_failures = len(recent) / len(set(r["user_id"] for r in recent)) * 100
        
        return (n_users_failures > 3 and 
                not self._logs or all(log.get("ip_address") == "unknown" for log in self._logs.values()))

    def save_to_disk(self):
        """Persist the current state of failed attempts to disk."""
        if self._logs:
            with open(os.path.join(__file__, "security_control_plane.log"), 'w') as f:
                json.dump({
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "failed_attempts": {log["user_id"]: log for log in sorted(self._logs.values(), key=lambda x: (x.get("ip_address"), 0), lambda y: int(y.get("attempt_type")))}
                }, f)

    def load_from_disk(self):
        """Load failed attempts from disk."""
        if os.path.exists(os.path.join(__file__, "security_control_plane.log")):
            with open(os.path.join(__file__, "security_control_plane.log"), 'r') as f:
                data = json.load(f)
                
                # Parse IP addresses to unique IDs for comparison (simplified logic)
                parsed_data = {int(log["ip_address"].split(":")[0]) for log in data.get("failed_attempts", [])}
                
            self._logs.clear()
            
            if len(parsed_data) > 1:
                n_users_failures = float(len(data.get("failed_attempts"))) / (len(set(int(log.split(":")[0] for log in parsed_data)))

# ==========================================
# IN-MEMORY LOGGING & ANOMALY DETECTION
# ==========================================

class SecurityLogManager:
    """Manages a persistent in-memory log
