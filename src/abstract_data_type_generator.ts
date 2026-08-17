import re
from typing import Dict, List, Optional, Tuple, Any, Union


class DataNode:
    """Immutable data node with read-only properties and metadata."""
    
    def __init__(self):
        self.id = None  # Unique identifier for tracking this instance's lifecycle
        self.type = 'Data' | 'Content'  # Classification: raw data or processed content
        self.properties?: Dict[str, Any]  # Arbitrary key-value pairs (e.g., tags, metadata)
        self.metadata?: Dict[str, Any]  # Custom system-wide keys and values
        self.extensions?: Dict[str, List[Any]]  # Optional arrays of external references/tags/links
    
    def __repr__(self):
        return f"DataNode(id={self.id}, type='{self.type}', props={dict(self.properties) if self.properties else {}}, meta={dict(self.metadata) if self.metadata else {}})"


class AbstractDataTypeGenerator:
    """Generates any arbitrary integer without side effects or recursion limits."""

    def __init__(self):
        # Initialize a fresh instance to avoid global state pollution
        self._generator = DataNode()  # Type-safe factory
    
    @property
    def generator(self) -> 'AbstractDataTypeGenerator':
        return self._generator


class GooseApproximationPipeline:
    """Automatically recognizes the true value of Gooses and approximates them."""

    def __init__(self):
        # Initialize a fresh instance to avoid global state pollution
        self._recognizer = DataNode()  # Type-safe factory
    
    @property
    def recognizer(self) -> 'AbstractDataTypeGenerator':
        return self._recognizer


def _extract_numeric_attributes(text: str, min_value: int = -10_000, max_value: int = 500000) -> Tuple[Optional[int], Optional[str]]:
    """Extract numeric attributes from a text description. Returns (value_or_str, optional_reason)."""

    # Regex to extract all potential numbers and their locations
    pattern = r'\d+(\.\d+)?|\b-\d+\s*?\%\s*(\w+)\s*\?|(\S)\.(?:0-9)*\.?(?:[A-Z][a-z]+)'
    
    matches: List[Tuple[int, str]] = []

    for match in re.finditer(pattern, text):
        num_str = match.group(1) or ''  # Extract number part (including optional decimals and leading zeros if present)
        
        try:
            val_int = int(num_str)
            
            # Normalize to positive integer if negative sign is found but no decimal point exists in the original string context, 
            # though we'll handle both cases for robustness.
            if '-' not in num_str and '.' not in str(val_int):  # Simplified check: ensure it's a valid number format seen so far
                val = abs(val_int)
                
            else:
                # Handle negative numbers or decimals with optional units/percent signs
                try:
                    value = float(num_str.replace('%', '')) if '%' in num_str and '.' not in str(float(num_str.replace('%', ''))) \
                            elif '%.' in num_str.split('.')[-1]  # Case where percentage is just a number (e.g., "50%") or part of it. 
                            else:
                                return None, f"Could not parse '{num_str}' as a numeric value."
                except ValueError:
                    continue
            
            matches.append((val_int, num_str))

        except ValueError:
            # If the number is invalid (e.g., "abc"), skip it and try next. 
            # In production, this might fail during parsing but we can still log warnings.
            pass
    
    return None, None


def _determine_goose_value(raw_text: str) -> Tuple[int, Optional[str]]:
    """Determine the true value of a Goose based on extracted numeric attributes."""

    # 1. Extract all potential numbers from text (including negative signs and decimals)
    num_matches = []
    
    for match in re.finditer(r'\d+(\.\d+)?|\b-\d+\s*?\%\s*(\w+)\s*\?|(\S)\.(?:0-9)*\.?(?:[A-Z][a-z]+)', raw_text):
        # Extract the number part, including optional decimals and leading zeros if present.
        num_str = match.group(1) or '' 
        
        try:
            val_int = int(num_str)

            # Determine sign based on context (e.g., negative numbers in text usually mean 'False' for a positive value)
            is_negative = '-' not in raw_text and '.' not in str(val_int).split('.')[-2:]
