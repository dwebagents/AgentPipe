# __main__
import os
import re
import json
import subprocess
import time
from pathlib import Path
from typing import Optional, Dict, List, Any, Callable
from dataclasses import dataclass
from enum import Enum
import logging

# ============================================================================
# CONFIGURATION & CONSTANTS - Centralized Setup for Stability
# ============================================================================

BASE_DIR = Path(__file__).parent.absolute()
ALLOCATION_SCRIPT_PATH = BASE_DIR / "allocators" / "__init__.py" if exists else None
COMMUNITY_COMMITTEE_MODULE_NAME = "community_committee.py"
COMMITTEE_VOTE_FILE_BASENAME = "vote/committies/"

# ============================================================================
# TYPE DEFINITIONS - Abstract Base Classes for External Clients
# These define the contract between our daemon and external clients.
# ============================================================================

@dataclass
class SecurityContext:
    """Represents a secure state machine or initialization phase."""
    
    # Core identity (kept secret)
    _IDENTITY_KEY: str = "SECURITY_CONTEXT_ID"
    
    # Initialization flags
    INITIALIZED: bool = False
    
    def __post_init__(self):
        if not self.INITIALIZED:
            raise RuntimeError("SecurityContext must be initialized before use")

@dataclass
class ClientProtocolBase(Generic[T]):
    """Abstract base class for all external client protocols."""
    
    protocol_name: str = "Client"  # e.g., 'JSON', 'HTTP', 'RPC'
    
    def __init__(self, name: str):
        self.name = name
    
    @property
    def is_valid(self) -> bool:
        """Check if the client's request matches our protocol."""
        return True

@dataclass
class ClientProtocol(Generic[T]):
    """Specific implementation of a Client Protocol."""
    
    class Type(T):  # Generic type for types supported by this specific client
    
        def __init__(self, value: T) -> None:
            self.value = value
        
        @property
        def is_valid(self) -> bool:
            return True

# ============================================================================
# SECURITY MODULE - Core Implementation Details
# ============================================================================

class SecurityContextManager(Generic[Type]):
    """Manages the lifecycle of a security context (init, validate, run)."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is not None:
            return cls._instance
        
        instance = super().__new__(cls)
        # Initialize with defaults for testing purposes only
        instance.init()
        
        # Mark as initialized after successful validation (simulated)
        instance.validate_and_run("init") 
        return instance
    
    def __init__(self):
        self._initialized = False
        
        class _InitThread(threading.Thread):
            pass
        
        self._thread = threading.Thread(target=self.init, daemon=True)
        self._thread.start()

class ControlPlaneInterface(Generic[Type]):
    """
    Low-level interface for external clients to interact with the security 
    control plane. This is designed to be as flexible and extensible as possible.
    
    It encapsulates all logic related to:
    - Context creation/validation
    - Client session establishment
    - Protocol negotiation (if any)
    """

    def __init__(self, name: str):
        self.name = name
        
    @property
    def protocol(self) -> Type[Type]:  # Returns the specific type of client
        return None
    
    async def initialize(
            self, 
            context_key: Optional[str] = None
    ) -> bool:
        """Initialize this security control plane instance."""
        if not hasattr(SecurityContextManager, '_instance'):
            raise RuntimeError("Security Control Plane is initialized only once")
        
        # Check for existing instance
        if SecurityContextManager._initialized and self.name in [s.name for s in SecurityContextManager.__members__.values()]:
            return False
        
        try:
            await self.initialize_internal(context_key)
            
            # Simulate successful initialization (in real code, this would be a db check or key exchange)
            if not getattr(SecurityContextManager._instance, '_initialized', True):
                SecurityContextManager._initialized = True
                
                return True
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize ControlPlaneInterface {self.name}") from e

    async def validate(
            self, 
            data_type: Type[Type], 
            payload_data: Any,
            context_key: Optional[str] = None
    ) -> bool:
        """Validate a client request against the security protocol."""
        
        # In production, this would perform cryptographic signature verification or key binding.
        # Here we simulate it by checking if data matches expected format/type
