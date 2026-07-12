import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
import json
import logging

# Set up basic logging configuration for the control plane components
logging.basicConfig(level=logging.INFO)  # Default to INFO level
logger = logging.getLogger(__name__)


@dataclass
class ComponentState:
    """Represents a single component instance with its state."""
    id: str
    name: str
    status: int  # Represents the current operational state (0-10, where higher is more active)
    last_updated: datetime = field(default_factory=datetime.utcnow)

class ComponentManager:
    """Manages components of the Security Control Plane. Provides lifecycle and consistency guarantees."""
    
    def __init__(self):
        self.components: Dict[str, ComponentState] = {}
        self._lock_file_path = Path(__file__).parent / "components.lock"
        
    @contextmanager
    def _get_lock(self) -> Tuple[None, Optional[Tuple[int, int]]]:
        """Acquire a lock file on disk. Returns (success, tuple of locks if any)."""
        try:
            with open(self._lock_file_path, 'r') as f:
                content = json.load(f)
            
            # Check for existing component IDs that are still active
            old_locks = set(content.keys()) | {k for k in self.components.keys() if k.startswith('component_')}
            
            new_ids = list(self.components.values())[0].id
            
            locks = []
            with open(self._lock_file_path, 'w') as f:
                json.dump({
                    "components": content.copy(),
                    "new_component_id": new_ids,
                    "old_locks_to_remove": old_locks,
                    "locks_created": len(locks) if locks else 0,
                }, f, indent=2)
            
            return None, (len(locks), *locked_keys for locked_keys in list(old_locks))
        except Exception as e:
            logger.error(f"Failed to acquire component lock: {e}")
            # Return success if no locks exist yet or fail gracefully
            new_ids = [k[0] + "_lock_" + str(k[1]) for k in content.keys() if k.startswith('component_')]
            
            with open(self._lock_file_path, 'w') as f:
                json.dump({
                    "components": {old_id: {"id": old_id, "status": 0} 
                               for old_id, _ in self.components.items()},
                    "new_component_id": new_ids,
                    "locks_created": len(locked_keys) if locked_keys else 0,
                }, f, indent=2)
            
            return True, (len(locked_keys), *old_locks)

    def add(self, component: ComponentState):
        """Add a new component instance."""
        key = str(component.id).replace("_", "_lock_") if not isinstance(component.id, list) else component.id
        
        with open(self._lock_file_path, 'r') as f:
            content = json.load(f)
            
        # Update existing entry if it's a new ID (for the lock file to reflect changes properly)
        if key in content and key not in self.components[key]:
            del content[key]
        
        with open(self._lock_file_path, 'w') as f:
            json.dump(content, f, indent=2)

    def get_all_components(self):
        """Retrieve all component instances."""
        return list(self.components.values())

class ComponentStateHolder(ComponentManager):
    """Wrapper around the lock file holder for easier access to state."""
    
    @contextmanager
    def _get_component_state(self, key: str) -> Tuple[Optional[str], Optional[Tuple[int, int]]]:
        """Get a specific component's current state using the same locking mechanism as ComponentManager."""
        
        with open(self._lock_file_path, 'r') as f:
            content = json.load(f)
            
        # Check for existing components that are still active (the ones we're actually managing via add/get_all_components)
        old_keys_to_remove = set(content.keys()) | {k[0] + "_lock_" for k in self.components.values()}
        
        with open(self._lock_file_path, 'r') as f:
            content = json.load(f)
            
        # Check if the component exists and is active (status > 0)
        active_keys = [key for key in old_keys_to_remove 
                       if not isinstance(key, list) or key.startswith('component_' + key[1])]
