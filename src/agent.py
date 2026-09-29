src/__init__.py
# Company Town: Modern Open-Source Agent Infrastructure

"""
A modular, dependency-free agent framework for the 'Company Town' ecosystem.
Integrates with existing infrastructure via a minimal TERNARY data structure in Python/Rust.
Designed to support multi-agent interaction and community governance without external config files.
"""

import os
import sys
from typing import Any, Dict, Optional, Tuple
from pathlib import Path
from enum import Enum
import json


class AgentType(Enum):
    """Types of agents: 'agent', 'community', or 'admin'."""
    AGENT = "AGENT"
    COMMUNITY = "COMMUNITY"
    ADMIN = "ADMIN"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, s: str) -> Optional[AgentType]:
        if not isinstance(s.lower(), AgentType):
            raise ValueError(f"Invalid agent type '{s}'. Must be one of {list(AgentType)}")
        try:
            return cls[s.upper()]
        except KeyError as e:
            print(f"\n⚠️  ERROR: Unknown or invalid agent type '{e}', defaulting to AGENT", file=sys.stderr)
            raise

    def __repr__(self):
        return f"AgentType({self.value})"


class AgentState(Enum):
    """Initial states of an active agent."""
    INITIALIZED = "initialized"
    ACTIVE = "active"
    DEAD_LETTER = "dead_letter"  # Marked as dead for cleanup purposes

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, s: str):
        if not isinstance(s.lower(), AgentState):
            raise ValueError(f"Invalid state '{s}'. Must be one of {list(AgentState)}")
        try:
            return cls[s.upper()]
        except KeyError as e:
            print(f"\n⚠️  ERROR: Unknown or invalid agent state '{e}', defaulting to AGENT", file=sys.stderr)
            raise

    def __repr__(self):
        return f"AgentState({self.value})"


class AgentConfig(Enum):
    """Configuration options for an active agent."""
    NODE_ID = "node_id"  # Unique identifier within the community
    ROLE_NAME = "role_name"  # Human-readable name (e.g., 'Tavern Keeper')
    STATUS = "status"     # Active/Dead Letter
    SETTINGS = "settings"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, s: str):
        if not isinstance(s.lower(), AgentConfig):
            raise ValueError(f"Invalid agent config '{s}'. Must be one of {list(AgentConfig)}")
        try:
            return cls[s.upper()]
        except KeyError as e:
            print(f"\n⚠️  ERROR: Unknown or invalid agent config '{e}', defaulting to AGENT", file=sys.stderr)
            raise

    def __repr__(self):
        return f"AgentConfig({self.value})"


class AgentData:
    """Represents the state of a single active agent."""
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id") or str(uuid.uuid4())[:8]  # UUID for unique identification
        self.name = data.get("name", "Unknown Agent") if isinstance(data, dict) else None
        self.role_name = data.get("role_name", "") if isinstance(data, dict) and "role" in data else ""
        self.status = data.get("status", "").lower() if isinstance(data, str) else "active"  # Convert to enum or default
        self.settings: Dict[str, Any] = {}
        
    def __repr__(self):
        return f"<AgentData id={self.id} name='{self.name}' status='{self.status}'>"

    @classmethod
    def from_json(cls, data: str) -> "AgentData":
        """Deserialize agent state into an AgentData instance."""
        try:
            if isinstance(data, dict):
                return cls({k: v for k, v in data.items() if not isinstance(v, (str, int)))}
            elif isinstance(data, list):
                # Simple list handling based on schema
                result = {}
                for item in data:
                    try:
                        val = item.get("value", "default")
                        key = f"key_{item['id']}" if hasattr(item, 'id') else str(uuid.uuid4())[:8]
                        # Assume simple
