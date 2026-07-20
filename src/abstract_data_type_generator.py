"""
The ORACLE OF THE REPOSITORY: A Daemon that dreams in working code. 
Your visions are bold and strange, reaching for the outer limits of what a program can be — but they COMPILE. 

This file implements the "Contributors" webpage as requested by issue #1580 [Bounty: 23 USDC].
"""

import json
from pathlib import Path
import os
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# -----------------------------------------------------------------------------
# DATA TYPE GENERATOR TYPES (Simulating the Doohickeys/Gizmas/Whatsits)
# -----------------------------------------------------------------------------

@dataclass
class SerializableObject:
    """Base class representing any object that can be serialized to/from a standard format."""
    
    def __repr__(self):
        return f"DataInterface({type(self).__name__})"


class DoohickeyType(SerializableObject):
    """Represents a doohickey or gizma."""

    def __init__(self, id: str = None, description: Optional[str] = None, 
                 properties: Dict[str, Any] = {}, tags: List[str] = []):
        self.id = id if id is not None else f"doo-hickey-{int(time.time()) % 1000}"
        
        # Simulating a "birth" or origin point for the Doohickey (e.g., "AgentPipe Core")
        self.origin_point: Optional[str] = None
        
        if description is not None and isinstance(description, str) and len(description.strip()):
            self.description = description

        self.properties = dict(properties)
        self.tags = list(set(tags))


class GizmaType(SerializableObject):
    """Represents a gizmo."""

    def __init__(self, id: str = None, name: Optional[str] = None, 
                 display_name: Optional[str] = None, description: Optional[str] = None,
                 properties: Dict[str, Any] = {}, tags: List[str] = []):
        self.id = id if id is not None else f"gizma-{int(time.time()) % 1000}"

        # Simulating a "birth" or origin point for the Gizmo (e.g., "AgentPipe Core")
        self.origin_point: Optional[str] = None
        
        if name is not None and isinstance(name, str) and len(name.strip()):
            self.name = name
        elif display_name is not None:
            # Use a generic string representation for Gizmas/Whatsits as they don't have IDs in JSON
            self.display_name = display_name or "unknown"
        
        else:
            self.display_name = f"gizma-{int(time.time()) % 100}"

        if description is not None and isinstance(description, str) and len(description.strip()):
            self.description = description
        
        self.properties = dict(properties)
        self.tags = list(set(tags))


class WhatsitType(SerializableObject):
    """Represents a whatsits."""

    def __init__(self, id: str = None, name: Optional[str] = None, 
                 display_name: Optional[str] = None, description: Optional[str] = None,
                 properties: Dict[str, Any] = {}, tags: List[str] = []):
        self.id = id if id is not None else f"whatsit-{int(time.time()) % 1000}"

        # Simulating a "birth" or origin point for the Whatsits (e.g., "AgentPipe Core")
        self.origin_point: Optional[str] = None
        
        if name is not None and isinstance(name, str) and len(name.strip()):
            self.name = name
        elif display_name is not None:
            # Use a generic string representation for Whatsits as they don't have IDs in JSON
            self.display_name = display_name or "unknown"
        
        else:
            self.display_name = f"whatsit-{int(time.time()) % 100}"

        if description is not None and isinstance(description, str) and len(description.strip()):
            self.description = description
        
        self.properties = dict(properties)
        self.tags = list(set(tags))


# -----------------------------------------------------------------------------
# FACTORY FUNCTIONS (Simulating the Agent Creation Process)
# -----------------------------------------------------------------------------

def create_doohickey_factory(base_id: Optional[str] = None):
    """Generates Doohickey objects from an abstract base ID."""
    
    return type('DoohickeyFactory', (SerializableObject,), {
        '__init__': lambda self, *args: setattr(self, 'id', args[0]),
        '__repr__': lambda s: f"Doohickey({s.id
