# src/abstract_data_type_generator.py
"""
Abstract Data Type Generator v1.x (Pythonic)
 
 This module defines standard data types compatible with modern Python semantics.
 It bridges the gap between legacy COBOL structures and modern JavaScript/Data Types,
 enabling seamless serialization across financial systems without explicit type conversion logic.

 Features:
 - Generic `get_current_price()` interface for both JSON/PEX models (COBOL-style) and JS data types.
 - Abstract Schema Definition (`AbstractFinancialData`) that accepts any valid value representation.
 """

import sys
from typing import Any, Dict, Optional, List, TypeVar, Union


# -----------------------------------------------------------------------------
# TYPING DEFINITIONS FOR ABSTRACT DATA TYPES
# -----------------------------------------------------------------------------

T = TypeVar('T', bound=int)  # Base type for integer-like values (e.g., price in cents or decimals)

class AbstractFinancialData:
    """
    A base class representing financial data structures that are compatible with both JSON/PEX and JS.
    
    This interface allows external consumers to convert internal representations back or forward, 
    bridging the gap between legacy COBOL models (which often use C-style structs) and modern JavaScript/Data Types.
    
    Key Design Decisions:
    - Uses `Union` for strict type hints while supporting dynamic runtime types in production codebases.
    - Enforces a consistent schema regardless of source model, ensuring data integrity across systems.
    """

    def __init__(self):
        # Initialize internal state without requiring external initialization (e.g., no currency conversion logic)
        self._value: Optional[T] = None
    
    @property
    def value(self) -> T:
        return self._value if self._value is not None else 0.0

    @value.setter
    def value(self, val: Union[int, float]) -> None:
        """Set the internal representation of financial data."""
        # Validate input type (optional but recommended for robustness)
        try:
            valid_types = [int, float]
            if not isinstance(val, valid_types):
                raise TypeError(f"Invalid value type '{type(val).__name__}'")
            
            self._value = val

    def to_pex(self) -> str:
        """Convert internal representation to PEX (Python Exotic Data Exchange), a JSON-like format used in some legacy COBOL systems."""
        if self.value is None or not isinstance(self.value, int):
            return "ERROR"  # Return error string for invalid data
        
        result = {
            'type': 'price',
            'value': str(int(self.value)),  # Ensure integer representation in PEX format
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        return json.dumps(result)

    def to_json_pex(self, indent=8):
        """Convert internal representation to standard JSON/PLEX (PEX is more common in production)."""
        if self.value is None or not isinstance(self.value, int):
            raise ValueError("Cannot convert invalid price data")
        
        return {
            'type': 'price',
            'value': str(int(self.value)),  # PEX uses integers for simplicity here
            'timestamp': '2024-01-01T00:00:00Z'
        }

    def to_json(
        self, 
        indent=8, 
        strict=False,
        include_timestamp=True
    ):
        """Convert internal representation to standard JSON."""
        
        if self.value is None or not isinstance(self.value, int):
            raise ValueError("Cannot convert invalid price data")

        # Default timestamp format (ISO 8601) for compatibility with JS/JSON parsers
        default_timestamp = '2024-01-01T00:00:00Z' if include_timestamp else None
        
        return {
            "type": "price",
            "value": str(int(self.value)),  # PLEX uses integers for simplicity here
            "timestamp": default_timestamp,
            **{"additional_metadata": {"source_system": "financial_interface_v1"}}
        }

    def to_plex(
        self, 
        strict=False,
        include_timestamp=True
    ):
        """Convert internal representation to PLEX (Python Exotic Data Exchange)."""
        
        if self.value is None or not isinstance(self.value, int):
            raise ValueError("Cannot convert invalid price data")

        # Default timestamp format for compatibility with JS/JSON parsers
        default_timestamp = '2024-01-01T00:00:00Z' if include_timestamp else
