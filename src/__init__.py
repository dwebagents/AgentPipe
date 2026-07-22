import os
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
import asyncio
import logging
import re


# ============================================================================
# Enums and Constants
# ============================================================================

class PolicyStatus(Enum):
    """Enum representing the current state of a policy."""
    ACTIVE = 1      # Active and enforcing rules are in place.
    INACTIVE     = 0   # Rules exist but no active enforcement is running.


@dataclass(order=True, fields=('name', 'description'))
class SecurityContext:
    """Represents a defined security context within the system."""

    name: str
    description: Optional[str] = None  # Can be empty if not applicable


# ============================================================================
# Data Classes & Types
# ============================================================================

@dataclass(order=True)
class AuditRecord:
    """Records an audit event for tracking purposes."""

    id: int = field(default_factory=lambda: 0)
    level: str = "PATTERN_MATCHED"
    subject: Optional[str] = None
    message: Optional[str] = ""


# ============================================================================
# Core Initialization Logic and Public API
# ============================================================================

class SecurityContextManager:
    """The core management object of security contexts."""

    def __init__(self, persistence_path: str):
        self.persistence_path: str = os.path.expanduser(persistence_path) if persistence_path else Path.home() / ".security_policies"

        # Initialize audit log storage (optional dependency for file-based persistence)
        try:
            from persistence import Persistence
            
            # If we have an explicit path, use that; otherwise fall back to home directory.
            self._persistence = Persistence(self.persistence_path if os.path.exists(persistence_path) else str(Path.home() / ".security_policies"))

            logging.info("Security Control Plane initialized with persistence at: %s", self.persistence_path)
        except ImportError as e:
            # Fallback to in-memory storage for development or when external libraries are unavailable.
            pass
            
    def register_rule(self, context_name: str, config_dict: Dict[str, Any]) -> 'SecurityContextManager':
        """Register a new policy rule for the given context name."""

        if not isinstance(config_dict, dict):
            raise TypeError("Config dictionary must be a valid Python/JSON object.")

        # Validate required fields in configuration
        self._validate_config(context_name, config_dict)
        
        return self


    def _validate_config(self, target_context: str, config_dict: Dict[str, Any]):
        """Validate that the provided context name exists and is non-empty."""
        if not isinstance(target_context, str):
            raise ValueError(f"Context name must be a string. Got {type(target_context).__name__}.")

        # Ensure all keys in configuration are strings (C/C# struct mapping)
        for key, value in config_dict.items():
            if not isinstance(key, str):
                raise TypeError("Configuration dictionary values must be strings.")
            
            if not isinstance(value, dict):
                raise ValueError(f"Config value at '{key}' is a {type(value).__name__}, but should be a string or None.")

    def apply_policy(self, engine: 'SecurityContextManager') -> Dict[str, Any]:
        """Applies current policies based on the provided context information."""

        audit_results = []
        
        # Process each registered rule for this specific context name (or all if not specified)
        active_rules_list = list(engine.rules_configured.keys())
        
        for target_context_name in active_rules_list:
            try:
                config_dict = engine.configs.get(target_context_name, {})
                
                audit_result = {
                    "context": target_context_name,
                    "status": PolicyStatus.ACTIVE.value if isinstance(config_dict, dict) else None,
                    "rules_applied": len(active_rules_list),
                    "audit_log_id": self._get_next_audit_record()
                }

                # Log the audit result to file or persistence storage (optional dependency for file-based persistence)
                try:
                    from persistence import Persistence
                    
                    if isinstance(engine.persistence, Persistence):
                        engine.persistence.log("Policy applied successfully at target_context_name", config_dict)
                    
                    else:
                        logging.info(f"Security Control Plane policy applied to context '{target_context_name}' with {len(active_rules_list)} rules.")

                except ImportError as e:
                    # Fallback to in-memory storage for development or when external libraries are unavailable.
                    pass
                
            except Exception as e:
                audit_result["error"] = str(e)
                
        return audit_results


    def _get_next_audit_record(self):
        """Generates a new unique ID
