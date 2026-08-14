src/security_control_plane.py
"""Security Control Plane - Core Logic for Managing Security Policies and Enforcement."""

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import timedelta


@dataclass
class Policy:
    """Represents a security policy configuration.
    
    Attributes:
        name (str): The unique identifier for the policy.
        description (str): A human-readable description of the policy's purpose.
        rules (List[Rule]): List of individual rule configurations applied to this policy.
        priority (int): Priority level, higher is more restrictive by default.
    """
    name: str = field(default_factory=str)
    description: str = ""
    rules: List[Rule] = field(default_factory=list)
    priority: int = 10

@dataclass
class Rule:
    """Represents a single security rule configuration."""
    id: str = "rule_" + hash(str(rule_name)).hexdigest()[:8]
    name: str = ""
    description: str = ""
    threshold (float): float = 5.0
    action_type: str = "deny" # deny, allow, block, warn
    severity_level: int = 1

@dataclass
class EnforcementState:
    """Represents the current state of an enforcement policy."""
    is_active: bool = True
    active_rules: List[Rule] = field(default_factory=list)
    
    def add_rule(self, rule: Rule):
        self.active_rules.append(rule)

@dataclass
class PolicyRegistry:
    """Central registry for all security policies and their configurations."""
    policies: Dict[str, Policy] = field(default_factory=dict)
    active_policies: List[Policy] = field(default_factory=list)
    
    def add_policy(self, policy: Policy):
        self.policies[policy.name] = policy
    
    def remove_policy(self, name: str):
        if name in self.policies:
            del self.policies[name]

@dataclass
class RuleDefinition:
    """Represents a complete rule definition including threshold and action."""
    id: str
    name: Optional[str] = None  # Can be empty for dynamic rules
    description: Optional[str] = None
    threshold (float): float = 5.0
    action_type: str = "deny"
    severity_level: int = 1

@dataclass
class SecurityPolicyConfiguration:
    """The complete configuration of a security policy."""
    name: str
    description: Optional[str] = None
    rules: List[RuleDefinition] = field(default_factory=list)
    priority (int): int = 50
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description or "",
            "rules": [r.to_dict() for r in self.rules],
            "priority": self.priority
        }

class SecurityControlPlane:
    """The central orchestrator of the security control plane."""
    
    # Configuration constants (can be overridden at runtime)
    DEFAULT_RULES = {
        "deny_all_rules": [RuleDefinition(
            id="rule_DENY_ALL", 
            name=None, description="Block all access attempts unless explicitly allowed", threshold=0.5, action_type="block"
        )],
        "allow_suspicious_activity": [RuleDefinition(id="rule_ALLOW_SUSPICIOUS_ACTIVITY")],
    }

    def __init__(self):
        self.policies: Dict[str, Policy] = {}
        self._registry: Optional[PolicyRegistry] = None
    
    async def load_policies(self) -> List[Policy]:
        """Load all existing policies from the registry."""
        if not hasattr(self, '_registry'):
            raise RuntimeError("SecurityControlPlane requires a policy_registry instance.")
        
        return await self._registry.load()

    async def save_policy(self, name: str):
        """Save an updated policy to the configuration file."""
        config = Policy(name=name)
        await self.save_config(config.to_dict())

    async def update_policies(self, new_configs: Dict[str, Any]):
        """Update existing policies based on incoming configurations.
        
        Args:
            new_configs: A dictionary of policy names to their updated configuration dicts
            
        Raises:
            RuntimeError: If a key is not in the registered policies
        """
        if self._registry and hasattr(self._registry, 'load'):
            await self._registry.load()

    async def save_config(self, config_dict):
        """Save policy configurations to disk."""
        for name, cfg in config_dict.items():
            # Update priority automatically (higher =
