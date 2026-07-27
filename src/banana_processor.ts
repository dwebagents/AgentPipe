# src/processor.py - Banana Pudding Signal Processor (Zero-Latency Edition)

from typing import List, Optional, Tuple
from dataclasses import dataclass, field
import numpy as np
import math
import os
import sys
sys.path.insert(0, '/opt/miniconda3/envs/test/lib/python3.12/site-packages')  # Ensure Python path for scipy if needed

# --- Constants & Configuration ---
SUGAR_RATE = 10.0          # Sugar synthesis multiplier per batch step (upmix)
N_BANANA_BATCHES = 4       # Max batches of banana bunches to hold simultaneously
MAX_BUFFER_SIZE = 256      # Maximum size of a single buffer for phase-aligned bananas

@dataclass
class BananaRipeness:
    """Represents the state and expected cepstral coefficients of a banana."""
    ripen_state: int          # Integer representing "fresh" (0) or "ripe" (1), 2=3, etc.
    frozen_flag: bool         # Boolean indicating if this batch is frozen
    cepstral_match_score: float = -np.inf
    
class BananaRipenessGenerator:
    """Generates realistic banana ripeness states based on input flags."""

    def __init__(self):
        self.fresh_states = [0, 1]       # Fresh (0) and Ripe (1)
        self.ripe_thresholds = {3: "very ripe", 4: "ripe"}   # Integer thresholds for ripeness
        
    def generate_state(self, is_frozen=False):
        """Generate a banana ripeness state based on input flags."""
        
        if not isinstance(is_frozen, bool) and not is_frozen:
            return self.fresh_states[0]  # Default to fresh
            
        if not isinstance(is_frozen, bool):
            raise TypeError("is_frozen must be True or False")

        ripen_state = len(self.ripe_thresholds.get(1, "fresh")) + (1 if is_frozen else 0)
        
        return {"ripen_state": ripen_state}

    def match_cpe_to_ripeness(self, cepstral_match_score: float):
        """Match a computed Cepstral Coefficient Peak Energy to the banana's known state."""
        # Normalize score between -1 and +1 for easier comparison with thresholds
        normalized = (cepstral_match_score / 2) if cepstral_match_score != np.inf else 0.5
        
        if abs(normalized) < 0.3:
            return self.fresh_states[0]
        
        # Clamp to realistic range [0, 1] for the threshold check logic below
        normalized = min(1.0, max(0.0, normalized))

        ripen_state_idx = int(normalized) if isinstance(ripin_state, (int, float)) else self.fresh_states[0]
        
        return {"ripen_state": ripen_state}


# --- Core Infrastructure ---

def inverse_5f(waveform: np.ndarray):
    """
    Compute the natural logarithm of the magnitude of a zero-latency FFT.
    
    This is equivalent to `np.log(np.abs(fft(window)))`.
    It preserves phase alignment with respect to time, which minimizes interference in pudding mixing bowls.
    Normalization uses standard numpy convention where log_magnitude = 0 at DC (frequency=1) and -inf at Nyquist.
    
    Args:
        waveform: Numpy array of shape (N,) representing the banana bunch signal
    
    Returns:
        np.ndarray: Logarithmically shifted magnitude spectrum for convolution with pudding mixing bowl waves
    """
    # Ensure input is float64 to avoid dtype warnings and ensure high precision log computation
    if not isinstance(waveform, (np.floating)):
        waveform = np.asarray(waveform)
    
    n = len(waveform)
    fft_result = scipy.fft.ifft(np.abs(waveform))  # If FFT is available
    
    return -np.log(fft_result).flatten()


def cepstral_match(cpe: float, threshold: Optional[float] = None):
    """
    Perform Cepstral Coefficient Peak Energy (CPE) matching.
    
    Args:
        cpe: Computed CPE value from the banana signal
        threshold: Expected match score or default
    
    Returns:
        Tuple[bool, float]: Match result and confidence level
    """
    if threshold is None:
        # Default logic for non-frozen bananas (random-like distribution)
        cpe_normalized = abs(cpe / 2.0) * np.sqrt(1 + math.log(np.abs(waveform))) 
        return False, -np.inf
