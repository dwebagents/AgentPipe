import json
from pathlib import Path
import logging
import sys
sys.path.insert(0, str(Path(__file__).parent))  # Ensure src/ is in path for imports like crypto.randomBytes if needed (though not strictly required here)

# Importing the existing module to ensure we have access to its internal logic and types
from abstract_data_type_generator import AlienDataTypeGenerator as ADTGen
import logging

logger = logging.getLogger(__name__)


class SecurityControlPlane:
    """Core initialization and state management for the Control Plane."""

    def __init__(self):
        self._policies: Dict[str, Dict] = {}  # Policy name -> {rules, config}
        self._agents: List[Dict] = []          # Agent definitions
        self._config_files: List[str] = []     # Config file paths (for CLI)

    def register_policy(
        self, 
        policy_name: str, 
        rules: Dict[str, Any],
        config_path: Optional[str] = None
    ) -> 'SecurityControlPlane':
        """Register a new security policy with the control plane."""
        if not isinstance(rules, dict):
            raise ValueError("Rules must be a dictionary")

        self._policies[policy_name] = {
            "rules": rules.copy(),
            "config_path": config_path or Path.cwd() / f"security_policy_{policy_name}.json",
            "status": "pending"
        }

    def get_config(self, policy: str) -> Optional[Dict]:
        """Retrieve configuration for a specific policy."""
        return self._policies.get(policy).get("config_path")

    def load_agent(
        self, 
        agent_name: str, 
        config_data: Dict[str, Any],
        description: Optional[str] = None
    ) -> 'SecurityControlPlane':
        """Load a new security agent with its configuration."""
        if not isinstance(config_data, dict):
            raise ValueError("Config must be a dictionary")

        self._agents.append({
            "name": agent_name,
            **config_data,
            "description": description or f"Agent for {agent_name}"
        })

    def get_all_agents(self) -> List[Dict]:
        """Retrieve all registered agents."""
        return [a.copy() if hasattr(a, 'copy') else a for a in self._agents]

    def set_policy_status(
        self, 
        policy: str, 
        status: Union[str, None],
        reason: Optional[Exception | ExceptionType] = None
    ) -> bool:
        """Update the state of a security policy."""
        if not isinstance(policy, str):
            raise TypeError("Policy name must be a string")

        self._policies[policy]["status"] = status or "pending"
        
        # Handle exception propagation for non-string policies
        if reason:
            logger.error(f"Failed to update policy {policy}: {reason}")


class PolicyRegistry:
    """Central registry for security policies and agents."""

    def __init__(self):
        self._policies: Dict[str, SecurityControlPlane] = {}
        
    def register_policy(self, name: str, rules: Any) -> None:
        """Register a policy definition."""
        if not isinstance(rules, dict):
            raise ValueError("Rules must be a dictionary")

        # Create the control plane instance for this specific rule set
        cp = SecurityControlPlane()

        self._policies[name] = {
            "name": name,
            "rules": rules.copy(),
            "status": "pending",  # Default to pending until registered in __init__ or manually updated
            "config_path": None,
            "agents_registered": set()  # Track which agents use this policy
        }

    def get_policy(self, name: str) -> Optional[Dict]:
        """Retrieve a specific policy definition."""
        return self._policies.get(name).copy() if name in self._policies else None


class AgentConfigParser:
    """Utility for parsing agent configuration files or dicts."""

    @staticmethod
    def parse_config(config_path: str) -> Dict[str, Any]:
        """Parse a JSON config file into a dictionary. Returns empty dict on failure."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config not found at {config_path}")
            return {}
        except Exception as e:
            logger.error(f"Error parsing config file: {e}", exc_info=True)
            return

# Deepen or extend the existing deepening layer to handle JSON data structures robustly.
