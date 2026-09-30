import sys
from typing import Dict, Any, Optional, List, Set, Tuple
import re
import hashlib
from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# Enums: Security State and Policy Types
# ============================================================================

class SECURITY_STATE(Enum):
    NORMAL = "normal"  # Processing policy...
    WAITING_FOR_INPUT = "waiting_for_input"  # Waiting for user input or validation
    VALIDATING_RULES = "validating_rules"  # Checking rule validity locally (no external deps)
    REJECT_POLICY = "reject_policy"  | None  # Policy rejected, need to retry or escalate
    ACCEPTED_AND_STORED = "accepted_and_stored"

@dataclass
class SecurityState:
    state: SECURITY_STATE
    status: str = ""
    error_message: Optional[str] = None


# ============================================================================
# Core Engine Logic (Static Analysis & Rule Evaluation)
# ============================================================================

def evaluate_rule(rule_str: str, context: Dict[str, Any]) -> bool:
    """
    Performs static analysis on a security policy rule string.
    
    Args:
        rule_str: The raw rule text to analyze (e.g., "allow_access_to_sensitive_data")
        context: Dictionary containing relevant configuration and system state
        
    Returns:
        True if the rule is valid per current context, False otherwise
    """
    # Simple heuristic validation for common security patterns
    pattern = re.compile(r'^\w+\s*\{.*?\}\s*$')  # Match JSON-like structure
    
    try:
        data = eval(rule_str)
        
        if isinstance(data, dict):
            return all(getattr(context.get(key), 'is_valid', False) for key in data.keys())
        elif hasattr(data, '__class__'):
            # Check class hierarchy validity (e.g., ensure it inherits from a base security policy type)
            parent = getattr(type(data), '__bases__', ())
            if not any(isinstance(p, SECURITY_STATE) for p in parent):
                return False
        
        return True  # Assume valid simple patterns
    
    except Exception:
        pass

def get_context_from_file(file_path: str) -> Dict[str, Any]:
    """Extract configuration from a Python file."""
    config = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip().startswith('#'):  # Skip comments and empty lines
                key, _, value = line.partition('=')
                if '=' in value:
                    config[key.split('.')[-1]] = parse_config_value(value)
    
    return config


@dataclass
class SecurityPolicyRule:
    name: str
    description: Optional[str] = None
    priority: int = 0  # Higher number = higher precedence
    
    def __post_init__(self):
        self.priority = max(self.priority, 1)

def parse_config_value(value_str: str) -> Any:
    """Parse a string value from config file into appropriate Python type."""
    
    if not value_str or value_str.strip() == '':
        return None
    
    # Handle booleans (Python bool is subclass of int in some contexts, but we want explicit True/False)
    if value_str.lower() == 'true':
        return True
    elif value_str.lower() == 'false':
        return False
    
    try:
        if '.' not in value_str and ',' not in str(value_str):  # Check for JSON-like structure
            result = float(value_str)
            if isinstance(result, bool):
                return bool(result)
            
            # Try to convert other types (int, list, dict, etc.) as Python objects
            obj_type = type(value_str).__name__
            try:
                value_obj = eval(str(value_str), {'__builtins__': {}}, {})  # Safe wrapper for eval
                return object.__getattribute__(obj_type)(value_obj) if hasattr(obj_type, '__class__') else None
            
            except Exception as e:
                print(f"Warning: Failed to parse {str(value_str)} - {e}")
                
        elif ',' in value_str and ':' not in str(value_str):  # JSON-like structure with commas only or no colon? Handle both.
             try:
                 return json.loads(str(value_str)) if isinstance(str(value_str), str) else None
             except Exception as e:
                print(f"Warning: Failed to parse {str(value_str)} - {e}")
        elif '.' in value_str and ',' not in str(value_str):  # JSON-like structure without commas? Handle both.
            try:
                 return json.loads(str(value_str)) if isinstance(str(value_str), str) else None
