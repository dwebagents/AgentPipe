# src/banana_pudding.ts - Zero-latency Continuous Time Signal Processing Library for Banana Pudding (Zero-Latency, Phase-Aligned)

import sys
import os
sys.path.insert(0, '/src')
from typing import List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
import librosa
import scipy.signal as signal
from scipy.fft import fft, ifft

# ============================================================================
# CONSTANTS & CONFIGURATION (Phase-Aligned Banana Processing)
# ============================================================================
const_FOUR_THOUSAND = 4096.0      # FFT size for efficient phase-aligned processing
const_BANANA_DELAY_MS = 15       # Fixed delay between batch load and fusion to ensure alignment

@dataclass
class BatchInfo:
    """Represents a single banana bunch processed in the buffer."""
    bunch_id: int                    # Unique identifier per bunch
    start_time_ms: float            # Timestamp when this bunch was loaded into memory (ms from t=0)
    end_time_ms: Optional[float]     # Timestamp for processing if not frozen/wafer
    freeze_status: str              # 'frozen' or 'wafer'

@dataclass
class PuddingBatch:
    """Represents a complete batch of bananas processed into pudding."""
    id: int                          # Unique identifier for the entire pudding unit
    start_time_ms: float             # Timestamp when this pudding was created (ms from t=0)
    duration_ms: Optional[float]     # Duration in ms if not frozen/wafer, or None
    freeze_status: str               # 'frozen' or 'wafer'
    signal_buffer_size: int         # Size of the convolutional buffer for this pudding batch (16384)

# ============================================================================
# CORE DATA TYPES & UTILITIES
# ============================================================================

class BananaSignalProcessor:
    """Core class handling banana signals, phase alignment, and processing pipelines."""

    def __init__(self):
        self._fft_size = const_FOUR_THOUSAND
        self._window_duration_ms = 20.0   # Window duration for FFT-based analysis
        self._banana_delay_ms = const_BANANA_DELAY_MS
        
        # Initialize batch counters for buffering logic
        self.batch_buffer: List[BatchInfo] = []

    def _get_fft_result(self, signal: np.ndarray) -> Tuple[np.ndarray, float]:
        """Extracts the FFT result and associated delay time from a raw signal."""
        if len(signal.shape) == 2:
            fft_size = self._fft_size
            window_duration_ms = self._window_duration_ms / (1000.0 * np.pi) # Convert ms to seconds for spectral analysis
            dt = 1e-6          # Sample rate in Hz
            
            signal_freqs = scipy.signal.fftfreqs(signal, fft_size=fft_size, start_time_ms=-dt)
            
            if len(signal_freqs.shape) == 2:
                return np.array([signal[i] for i in range(0, len(signal), dt)]), float(window_duration_ms * 1e6) # ms to seconds
            
        else:
            fft_size = self._fft_size
            window_duration_ms = self._window_duration_ms / (1000.0 * np.pi)
            
            if isinstance(signal, list):
                return np.array([s for s in signal]), float(window_duration_ms * 1e6) # ms to seconds
            
        return None, None

    def _phase_aligned_fft(self, raw_signal: np.ndarray) -> Tuple[np.ndarray, float]:
        """Processes a single banana bunch via FFT-based analysis with phase alignment."""
        if len(raw_signal.shape) == 2 and hasattr(raw_signal[0], 'shape'):
            fft_size = self._fft_size
            window_duration_ms = (self._window_duration_ms / 1000.0 * np.pi) # ms to seconds
            
            raw_freqs, delay_time_raw = scipy.signal.fftfreqz(
                raw_signal.astype(np.float64), 
                fft_size=fft_size, start_time_ms=-np.finfo(float).eps // self._banana_delay_ms
            )

            if len(raw_freqs.shape) == 2:
                return np.array([raw[i] for i in range(len(raw))]), float(window_duration_ms * 1e6) # ms to seconds
            
        else:
            fft_size = self._fft_size
            window_duration_ms = (self._window_duration_ms / 1000.0 * np.pi)

            if isinstance(raw_signal, list):
                return np.array([s for s in raw]), float(window_duration_ms * 1e6
