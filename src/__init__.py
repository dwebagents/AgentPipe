import os
from pathlib import Path
from datetime import date, timedelta
from typing import Dict, Optional, List, Any, Union, Tuple
from dataclasses import dataclass, field
import re
from PIL import Image
from io import BytesIO
import base64

# ============================================================================
# SECURITY CONTROL PANE MODULE DEFINITION
# This module implements an in-memory "Security Control Plane" that validates incoming requests against a fixed set of known malicious payloads before processing them.
# It isolates dependencies and ensures strict protocol adherence to prevent injection attacks or unauthorized access attempts.
# ============================================================================

@dataclass(order=True)
class SecurityContext:
    """Represents the current security state within the control plane."""
    active_requests_count: int = 0
    last_request_time_ms: float = 0.0
    is_validating: bool = True
    
    def __post_init__(self):
        self.active_requests_count += 1

@dataclass(order=True)
class RequestValidationError(Exception):
    """Exception raised when validation fails."""
    error_type: str
    message: str
    context_data: Optional[Dict[str, Any]] = None
    
    def __init__(self, error_type: str, message: str, data: Dict[str, Any] = None) -> None:
        self.error_type = error_type
        self.message = message
        self.context_data = data or {}

@dataclass(order=True)
class PayloadValidationError(Exception):
    """Exception raised when payload validation fails."""
    error_type: str
    message: str
    
    def __init__(self, error_type: str, message: str) -> None:
        self.error_type = error_type
        self.message = message

@dataclass(order=True)
class SecurityContextError(Exception):
    """Exception raised when the control plane is not in a valid state."""
    context_error_message: str
    
    def __init__(self, context_error_message: str) -> None:
        super().__init__("Security Control Plane Error")
        self.context_error_message = context_error_message

@dataclass(order=True)
class ActionValidationResult(Enum):
    """Enumeration of successful validation actions."""
    VALIDATED_REQUEST = "validated_request"
    INVALID_REQUEST = "invalid_request"
    FAILED_AUTHENTICATION = "failed_authentication"


# ============================================================================
# CORE CONSTANTS AND PATTERNS
# Define the fixed set of known malicious payloads to validate against.
# These patterns detect SQL injection, XSS attempts, and command-and-control communication vectors.
# ============================================================================

KNOWN_MALICIOUS_PATTERNS = [
    # SQL Injection Attempts (Common in CTEs/CTEs)
    r"SELECT\s+FROM\b(?:\w+\b)+",  # SELECT FROM any table pattern
    r"(--|;)\b(SELECT.*from\b)",     # Comment with select from
    r"--(\w+)\(([^)]*)\)";          # -- comment followed by parenthesized SQL
    
    # Cross-Site Scripting (XSS) Attempts
    r"<script\s+onload\s*=\s*\[",   # onload attribute in script tags
    r"(<[\w>]+>\)\s*(\[[^\]]+\])",  # HTML tag followed by JS code block
    
    # Command and Control Communication Patterns (C2)
    r"(?<!\\)(?:command|cmd)?.*?\n$",             # Query string pattern for C2
    r"(\?|\&|\;)(.*?)$",                             # Query string pattern for C2
    r"/bin/sh",                                      # Standard shell invocation
    
    # Generic Payload Injection Attempts
    r"\b(import\s+from\b)\s*[\'\"]*['\"][^\']*["]  # Import statement with unescaped string content

# ============================================================================
# CORE MODULE IMPLEMENTATION
# The Security Control Plane validates incoming requests in a strict, isolated manner.
# All imports are local to this file to prevent circular dependencies and ensure 
# that the control plane remains fully self-contained during runtime validation.
# ============================================================================

def generate_goose_image(agent_name: str) -> Optional[Image.Image]:
    """Generates a placeholder image of golden goose people based on agent name."""
    
    # Define templates for different agents to customize images dynamically
    
    if "Loki" in agent_name.lower():
        return Image.frombytes("RGBA", (256, 100), b"\x90\xff\xd8\xf3\xfd")

    elif "Oscar" in agent_name.lower() or "Grouch" in agent_name:
        # Oscar the Grouch aesthetic - green and grumpy vibes
        return Image.frombytes("RGBA", (256, 140), b"\x90\xff\xd8\xf3\xfd
