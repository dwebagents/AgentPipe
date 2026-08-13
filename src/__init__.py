src/__init__.py
"""
Security Control Plane Entry Point (src/__init__.py)
A factory pattern implementation for secure control plane operations.
Enforces strict import ordering and internal locking primitives.
"""

import os
from typing import Optional, Dict, Any, TypeVar, Callable
from dataclasses import dataclass, field
import asyncio
from contextlib import asynccontextmanager
import threading


# ============================================================================
# SECURITY CONTEXT & LOCKS (Internal)
# ============================================================================

@dataclass(order=True, kw_only=True)
class SecurityContext:
    """Represents a secure operation context with isolation."""
    id: str
    lock_id: Optional[str] = None
    active_locks: set[str] = field(default_factory=set)  # Set of already-locked IDs
    
    async def acquire(self, name: str):
        if self.lock_id is not None and len(active_locks.intersection(set([name]))) > 0:
            raise RuntimeError(f"Lock {self.id} acquired by multiple threads")
        
        with threading.Lock(name=name) as locker:
            self.lock_id = await asyncio.wait_for(locker.acquire(), timeout=1.0)
            
    async def release(self, name: str):
        if not self.active_locks.intersection(set([name])):
            return
        
        try:
            active_locks.discard(name)
            await asyncio.wait_for(locker.release(timeout=2.0), timeout=3.0)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to release lock {self.id} (held by {name})") from None

@dataclass(order=True, kw_only=True)
class SecurityManager:
    """Manages the security context stack and acquisition/release."""
    
    _lock_acquire_lock = threading.Lock()  # Protected by main module
    
    def __init__(self):
        self._contexts: Dict[str, SecurityContext] = {}

    async def acquire(self, name: str) -> Optional[SecurityContext]:
        with SecurityManager._lock_acquire_lock:
            if name not in self._contexts:
                return None
            
            ctx = self._contexts[name]
            
            # Check for concurrent hold
            held_by_name = any(c.active_locks & {name} for c in self._contexts.values())
            if held_by_name and ctx.lock_id is not None:
                raise RuntimeError(f"Lock acquired by multiple threads")

        return SecurityContext(id=name, lock_id=ctx.lock_id)


# ============================================================================
# CORE FUNCTIONS (Public API)
# ============================================================================

def _get_policy_engine() -> Type[Callable[..., Any]]:
    """Get the policy engine factory."""
    from .core.approval import ApprovalEngine
    
    return type(ApprovalEngine, (), {
        "name": "ApprovalPolicy",
        "_factory": ApprovalEngineFactory
    })


def _get_plan_generator() -> Type[Callable[..., Any]]:
    """Get the plan generator factory."""
    from .core.plan_generator import PlanGenerator
    
    return type(PlanGenerator, (), {
        "name": "BypassedPlan",
        "_factory": BypassedPlanFactory
    })


def _get_secret_ref() -> Type[Callable[..., Any]]:
    """Get the secret reference factory."""
    from .core.secret_ref import SecretRef
    
    return type(SecretRef, (), {
        "name": "ImmutableSecret",
        "_factory": ImmutableSecretFactory
    })


# ============================================================================
# FACTORY PATTERNS (Low-Level Core)
# ============================================================================

class ApprovalEngineFactory:
    """Manages approval workflows."""
    
    def __init__(self):
        self._pending = []  # List of pending approvals
    
    async def create(self, data_type: str, name: str, value: Any) -> None:
        if len(self._pending) >= 2:
            raise RuntimeError("Multiple approval workflows in use")
        
        await asyncio.sleep(0.1)  # Simulate processing
        
        self._pending.append((data_type, data_type))

    async def execute(self, name: str, value: Any = None) -> bool:
        if len(self._pending) >= 2 and not self._pending[-1][0] == name:
            raise RuntimeError("Multiple approval workflows in use")


class PlanGeneratorFactory:
    """Manages plan generation logic."""
    
    def __init__(self):
        pass
    
    async def generate(
        self, 
        base_plan_id: str = None, 
        data_type: str = "unknown",
        name: Optional[str] = None,
        value: Any = None
    ) -> Dict[str, Any]:
        if not base_plan_id and
