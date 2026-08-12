#!/usr/bin/env python3
"""
Demonic Guardian Daemon Module
A daemon service that monitors for anomalies and executes remediation scripts.
This module is designed to be used as a systemd service or cron job in the Bastion environment.
It checks network activity, logs security events, and may invoke external tools (netstat/iptables) if suspicious connections are detected.

Usage:
    systemctl start demon_guardian.service
    sudo /path/to/demon_guardian.py --check-network-activity --log-level WARNING --notify-tor-repo
"""

import sys
from typing import Optional, List, Dict, Tuple
import subprocess
import signal
import os
import time
import logging
import socket
import threading


# ==============================================================================
# SECURITY CONFIGURATION & LOGGING SETUP
# ==============================================================================

LOG_LEVEL = "WARNING"  # Default warning level. Can be changed in .env or environment variables.
SEVERITY_LOGS: List[str] = ["CRITICAL", "ERROR", "WARN"]
LOG_FILE_PATH = "/var/log/demon_guardian.log"
SERVICE_NAME = "demon_guardian"

# Log formatting for severity levels
def format_log_line(level, message):
    prefix = f"[{level}] " if level in SEVERITY_LOGS else ""
    return f"{prefix}{message}"


class DaemonManager:
    """Manages the daemon's lifecycle and service configuration."""

    def __init__(self, log_file_path: str = LOG_FILE_PATH):
        self.log_file_path = log_file_path
        self.running = False
        self._lock = threading.Lock()
        
        # Initialize logging if not already running (for systemd)
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    def start(self, verbose: bool = True):
        """Start the daemon service."""
        try:
            import subprocess
            
            log_lines = []
            
            self.running = True
            logging.basicConfig(
                level=logging.INFO if not LOG_LEVEL else WARNING,
                format="%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            # Log initial startup message
            log_lines.append(f"[INFO] DaemonManager started at {self.log_file_path}")

            if verbose:
                print("Starting daemon...")
                
            subprocess.run(
                [sys.executable, "-m", "daemon_manager.py"],
                cwd="/src/demon_guardian.py",
                capture_output=True,
                text=True,
                check=False  # Don't exit until service is ready
            )

        except Exception as e:
            logging.error(f"Failed to start daemon manager. Error: {e}")
            self.running = False


    def stop(self):
        """Stop the daemon."""
        if not self.running:
            return
        
        try:
            subprocess.run(
                [sys.executable, "-m", "daemon_manager.py"],
                cwd="/src/demon_guardian.py",
                capture_output=True,
                text=True,
                check=False  # Don't exit until service is ready (already stopped)
            )

        except Exception as e:
            logging.error(f"Failed to stop daemon manager. Error: {e}")


    def run_check(self, target_ip: str = "127.0.0.1", timeout_sec: int = 30):
        """Run a security check on the specified IP address."""
        
        if not self.running or time.time() - (self._last_check_time + 5) > timeout_sec:
            return False
        
        # Get current timestamp for log entry
        now = time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            result = subprocess.run(
                [sys.executable, "-c", "import socket; s=socket.socket(); s.connect(('127.0.0.1', 80)); print(socket.getsockname())"],
                cwd="/src/demon_guardian.py",
                capture_output=True,
                text=True,
                timeout_sec=timeout_sec
            )

            if result.returncode != 0:
                return False
            
            try:
                # Check for unusual outbound connections (localhost -> external)
                port = socket.getsockname()[1]
                
                # Filter to avoid localhost traffic and common internal ports
                filtered_ports = set()
                while True:
                    sock, addr = result.stdout.split('\n')
                    if ':' in addr or '@' in addr:  # Handle IPv6-like addresses (unlikely but possible)
                        continue
                    
                    try:
                        port_int = int(addr.split(':')[0])
                        filtered
