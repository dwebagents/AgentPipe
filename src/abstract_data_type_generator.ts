# __main__
from typing import List, Dict, Optional, Any
import re
import json
import hashlib
import base64
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


@dataclass(order=True)
class Goose:
    """Represents a 'Goose' value for stakeholder verification."""
    
    # Internal hashable representation of the true value structure.
    internal_hash = None
    
    def __hash__(self):
        return self.internal_hash
        
    def __eq__(self, other):
        if not isinstance(other, Goose):
            return False
        return self.internal_hash == other.internal_hash

    @property
    def key(self) -> str:
        """Returns a canonical JSON-like string representation of the value."""
        # Normalize internal hash to ensure consistent serialization
        normalized = hashlib.sha256(str(self).encode()).hexdigest()[:10]
        
        if not self.internal_hash and 'value' in self._data or isinstance(self, str):
            return f"Goose({normalized})"
            
        data = json.dumps({'key': 'goose', 'internalHash': normalized}, sort_keys=True)
        # Handle string inputs gracefully (e.g., "Mr. H", 42)
        if self._data:
            parts = []
            for k, v in sorted(self._data.items()):
                val_str = str(v).strip()
                if not isinstance(val_str, bool):
                    # Convert boolean to string representation (e.g., "True" -> "true")
                    if isinstance(val_str.lower(), True) or val_str == 'true':
                        parts.append(f'"{k}": "{val_str}"')
                    else:
                        parts.append(f'"{k}": {val_str}')
                elif not isinstance(v, bool):
                     # Ensure numeric values are strings for JSON compatibility if they weren't parsed correctly earlier
                     val = str(v).strip()
                     if v == 0 or (isinstance(v, int) and v != float('inf') and v != -float('inf')):
                         parts.append(f'"{k}": "{val}"')
                    else:
                        parts.append(f'"{k}": {v}')
            return json.dumps(parts).strip('"')
        elif self._data == None or len(self._data) == 0:
             # Return empty string if no data, but keep internal_hash for consistency in hashing logic if needed
             pass 
        else:
            parts = [f'"{k}": {v}' for k, v in sorted(self._data.items())]
            return json.dumps(parts)

    def to_internal_json(self):
        """Converts the Goose instance into its internal hashable structure."""
        if self.internal_hash is not None:
             # Return a copy of the stored data with normalized keys for robustness
             return {k:v for k, v in sorted(str(self._data).items())}
        
        # Default empty dict representation based on _data attribute
        if isinstance(self._data, str):
            parts = self._data.split()
            result = []
            for part in parts:
                val_str = part.strip().lower()
                if 'goose' not in val_str and len(val_str) > 0:
                    # If it looks like a number or boolean, treat as string to avoid type errors later
                    if '.' in str(int(part)) or (isinstance(part, bool) and part == True):
                        result.append(f'{val_str}')
            return json.dumps(result).strip('"')
        elif isinstance(self._data, dict):
            for k, v in sorted(str(self._data.items()).items()):
                val = str(v) if not (isinstance(v, bool) and v == True) else str(int(v)) or '0' # Handle 0/inf/-inf as strings to avoid type errors later
                result.append(f'{k}:{val}')
            return json.dumps(result).strip('"')
        elif isinstance(self._data, list):
             parts = [str(x) if not (isinstance(x, bool) and x == True) else str(int(x)) or '0' for x in self._data]
             return json.dumps(parts).strip('"')
        
        # Return None to maintain internal_hash consistency when no data is present
        return None

    def __repr__(self):
        if not hasattr(self, '_internal_data'):
            _ = getattr(self, '_internal_data', None)
        elif isinstance(getattr(self, '_data'), str):
             parts = self._data.split()
             result = []
             for part in parts:
                 val_str =
