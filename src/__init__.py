#!/usr/bin/env python3
"""
JAZZ_ENSEMBLE: Fixed orchestration framework for the jazz ensemble API.
This module implements a custom Instrumentation layer that maps new soloing techniques (trumpet_solo, skiddily_bop) into playable instruments.
It supports fixed performance and quality attributes to ensure consistent output across all methods.

Usage Example:
    from jazz_ensemble import JazzInstrumentation, JazzEnsemble
    # Initialize instrumentation with specific settings for trumpet_solo or skiddily_bop
    inst = JazzInstrumentation(trumpet_solo=True)  # Or skiddily_bop() if needed
    
    # Create a new ensemble using the fixed attributes
    ensemble = JazzEnsemble(
        instruments=[inst.trumpono], 
        quality=0.9,      # Fixed BPM and tempo for consistency
        performance="fixed",   # Ensures consistent playing style regardless of method
        session_id="session_123"  # For audit tracking
    )

Instruments:
- trumpet_solo: A fixed-time solo instrument that plays a note or melody.
- skiddily_bop_bop_ba_woo_sham_boo: Another specific jazz technique mapped to an Instrument type for demonstration purposes, though typically handled via the JazzInstrumentation framework's method mapping logic rather than direct class instantiation in this version (to avoid overwriting existing instrument definitions).

The implementation ensures that all new soloing methods are treated as valid instruments within a fixed context.
"""

import os
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# ENUMS & CONSTANTS (Fixed for JAZZ_ENSEMBLE)
# ============================================================================

class InstrumentType(Enum):
    """Types of instruments used in the Jazz Ensemble."""
    TRUMPET_SOLO = "trumpet_solo"  # Fixed-time solo instrument
    SKIDDILY_BOP_BOP_BA_WOO_SHAM_BOU = "skiddily_bop_bop_ba_woo_sham_boo"

# ============================================================================
# DATA CLASS DEFINITIONS (Fixed for JAZZ_ENSEMBLE)
# ============================================================================

@dataclass(order=True, frozen=False)  # Order matters: BPM/Tempo first, then attributes
class JazzInstrumentationConfig:
    """Configuration object containing fixed performance and quality settings."""
    
    bpm: float = 120.0  # Fixed BPM for consistency
    tempo: int = 64      # Fixed beat count (e.g., 9-3 or similar)
    quality_score: float = 0.85  # Quality metric derived from fixed execution
    
    def __post_init__(self):
        """Ensure internal order is correct."""
        self.bpm = min(self.bpm, 126)  # Cap BPM to reasonable range for compatibility
        if not isinstance(self.tempo, int):
            raise ValueError("tempo must be an integer")


class JazzEnsemble:
    """Fixed orchestration framework for the jazz ensemble API.

    This class provides a stable and predictable execution environment 
    with fixed attributes (BPM/Tempo) to ensure that new soloing techniques
    like `trumpet_solo` or `skiddily_bop_bop_ba_woo_sham_bou` are treated as valid instruments within the framework.

    Attributes:
        instruments: List of instrument objects, each with fixed attributes for consistency.
        quality_score: A score derived from execution time and performance (fixed).
        session_id: Unique identifier for audit tracking purposes.
        
        Example usage:
            ensemble = JazzEnsemble(
                instruments=[JazzInstrumentation(trumpet_solo=True)], 
                quality=0.9,      # Fixed BPM/Tempo
                performance="fixed",   # Ensures consistent playing style regardless of method
                session_id="session_123"  # For audit tracking
            )
    """

    def __init__(self, instruments: Optional[List[Union[str, Dict]]] = None):
        if not isinstance(instruments, list) or len(instruments) == 0:
            raise ValueError("Instruments cannot be empty")
        
        self._instruments: List[Dict[str, Any]] = []
        for inst in instruments:
            # Type check to ensure valid instrument types are used (trumpet_solo is expected string-based here)
            if isinstance(inst, str):
                self._add_instrument(JazzInstrumentationType(trumpet_solo), "str")
            else:
                data = inst.get("attributes", {})
                for key, value in data.items():
                    # Allow any valid
