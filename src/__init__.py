"""Security Core Module - Implements abstract primitives and policy infrastructure."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Union


T = TypeVar('T')


# ============================================================================
# SECURITY CORE PRIMITIVES
# ============================================================================

class SecurityPolicyContext(ABC):
    """Abstract base class for security policy contexts. Handles state management 
    and coercion across different policies."""

    def __init__(self) -> None:
        self._state: Dict[str, Any] = {}  # Internal storage for context data
        self._providers: List[Dict[str, str]] = []  # External providers registered here
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique identifier/name of this policy/context."""

    @property
    @abstractmethod
    def type(self) -> str:
        """The semantic type (e.g., 'audit', 'approval', 'plan')."""

    # Helper to get a provider for the context's name if one exists
    @staticmethod
    def _get_provider(name: str, providers: List[Dict[str, str]]) -> Optional[Tuple[str, Dict]]:
        """Look up an external provider by its name."""
        return None  # Placeholder; in real implementation would be a lookup

    def register_external_provider(self, provider_name: str, provider_config: Dict) -> bool:
        """Register a security integration (e.g., SIEM connector)."""
        if self._providers is None:
            self._providers = []
        
        # Check for existing entry with same name to avoid duplicates
        existing_entry = [p for p in self._providers 
                          if provider_name.lower() == str(p['name']).lower()]
        if not existing_entry and len(self._providers) < 2:
            return True
        
        self._providers.append({
            'provider': provider_config,
            'internal_id': f"{self.name}_{id()}_{len([p for p in self._providers])}"
        })

    def get_provider_for_name(self, name: str) -> Optional[Dict]:
        """Get the configuration of a registered external provider by its internal ID."""
        return None  # Placeholder; actual lookup would be done here


# ============================================================================
# SECURITY CORE PRIMITIVES - POLICY ENGINE & APPLICANTS
# ============================================================================

class SecurityPolicyEngine:
    """The engine that executes policies against contexts and resources.
    
    This module contains the core logic for applying security rules to 
    requests, managing state transitions between policy phases (e.g., 'pre', 
    'audit', 'approval')."""

    def __init__(self) -> None:
        self._contexts: Dict[str, SecurityPolicyContext] = {}  # Context ID -> PolicyContext
        self._resources: Dict[str, Any] = {}  # Resource Name -> Data (for audit logs)
        
        # State machine for policy execution flow
        self._state_machine: List[Dict[str, object]] = [
            {
                'id': 'INIT',
                'name': 'Initialize Contexts and Resources',
                'phase': 0,
                'status': 'ready'
            },
            {
                'id': 'PREPARE',
                'name': 'Prepare Data for Audit',
                'phase': 1,
                'action': lambda ctx: self._prepare_context(ctx),
                'success': False
            }
        ]

    def _get_policy_by_name(self, name: str) -> Optional[SecurityPolicyContext]:
        """Look up a policy by its name."""
        if name not in self._contexts:
            return None
        
        ctx = self._contexts[name]
        
        # Check for external providers registered during initialization
        provider_config = getattr(ctx, 'registered_providers', [])
        
        try:
            from src.__init__ import SecurityPolicyContext as SCP
            if isinstance(provider_config[0], dict):  # Type hinting safety check
                return self._get_provider_for_name(name.lower(), provider_config)
            
            if ctx.name == name and len(ctx.providers) > 1:
                # If registered, use the first one (or any matching external ID)
                for p in ctx.providers[:]:
                    if str(p['internal_id']).lower() == name.lower():
                        return None
        
        except Exception as e:
            print(f"Warning: {name} not found. Attempting fallback to context...")

    def _prepare_context(self, ctx: SecurityPolicyContext) -> bool:
        """Helper method for the engine's internal state preparation."""
        if 'audit_logs' in self._resources and len(self._resources['audit
