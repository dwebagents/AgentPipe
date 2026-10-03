"""Security Control Plane Implementation."""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
import logging
from typing import Any, Dict, List, Optional, Tuple, Union
import sys
sys.path.insert(0, '/src')  # Ensure imports work from the module level if needed for testing context

# --- Log Setup & Configuration ---
logger = logging.getLogger(__name__)


class SecurityControlPlane(ABC):
    """Abstract base class representing a generic security control plane.
    
    This is an abstraction layer that defines how different components of 
    the security architecture interact and manage state transitions between phases:
      - Prep (Preparation)
      - Execute (Execution/Processing)
      - Post (Post-Processing / Verification)
    """

    @abstractmethod
    def initialize(self, config_path: str = None):
        """Initialize this instance with configuration data. 
        Must be called once to establish the base state for all components."""
        pass
    
    @abstractmethod
    def run_phase(
        self, phase_name: str, 
        context_data: Dict[str, Any] = None,
        log_message: Optional[str] = None
    ) -> Tuple[bool, List[str]]:  # (success_flag, error_log)
        """Execute a specific security phase.
        
        Args:
            phase_name: The name of the current execution stage ("Prep", "Execute", or "Post").
            context_data: Optional dictionary containing additional metadata about this step's parameters 
                           and validation requirements. If None, will default to empty data structures.
            log_message: An optional string describing what is happening during this phase (for debugging).

        Returns:
            Tuple of (is_success, error_log) where success indicates the phase was completed or handled without failure.
            
        Raises:
            ValueError: If context_data is missing required keys that are expected for specific phases.
            RuntimeError: If a critical security policy cannot be applied at this stage.
        """
        pass

    @abstractmethod
    def validate_policy(self, rule_key: str) -> bool:
        """Check if the current state satisfies all applicable policies and rules.
        
        Args:
            rule_key: The unique identifier of a specific security policy or constraint (e.g., 'min_users', 
                       'max_latency_seconds', etc.). This is used to query external configuration files, 
                       mock databases, or check against stored artifacts.

        Returns:
            bool indicating whether the current state meets all validation criteria for this rule.
            
        Raises:
            ValueError: If a required policy parameter (like min_users) is not present in context_data.
            RuntimeError: If enforcing policies results in an impossible configuration.
        """
        pass

    @abstractmethod
    def get_state_summary(self, phase_name: str = None) -> Dict[str, Any]:
        """Retrieve and return a summary of the current state for debugging or reporting purposes.
        
        Args:
            phase_name (str): Optional filter to only include data from specific phases 
                              ("Prep", "Execute", "Post"). If not provided, returns all active states.

        Returns:
            Dictionary containing summaries of security metrics and rule violations across the entire lifecycle.
            
        Raises:
            RuntimeError: If a critical component (e.g., 'audit_engine', 'policy_checker') is unavailable or in an error state.
        """
        pass


class PolicyChecker(PolicyChecker):
    """Utility class for validating incoming security rules against the current context."""

    def __init__(self, config_path: str = None):
        super().__init__()
        
        # Load configuration from file if provided, otherwise fall back to default mock data
        self.config_data = {}
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    key, value = line.strip().split(':', 1)
                    # Split on the first ':' only (for simplicity), or split by colon if needed later.
                    self.config_data[key] = value.split('"', 1)[0].strip()
        except FileNotFoundError:
            pass

    def _validate_rule(self, rule_key: str) -> Dict[str, Any]:
        """Internal helper to validate a specific policy without exposing the full config."""
        
        # Simulate loading from file or mock data if not found
        try:
            self.config_data = {k: v for k, v in self.config_data.items() 
                               if rule_key.lower().startswith(k.lower())}
        except Exception as e:
            logger.warning(f"Failed to load policy config for '{rule_key}' due to file access error. "
                          f"{str(e)}")

        return {k: v for k, v
