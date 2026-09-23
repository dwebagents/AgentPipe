# -*- coding: utf-8 -*-
"""
Source Files for src/banana_pudding.py
Core Signal Processing Module and Sugar Synthesis Utility.
This module implements phase-aligned banana bunches, cepstral normalization logic, 
multichannel upmixer generation using multiplicative synthesis, 
and a convolver class that applies unnatural logarithms to Mason jar data before convolution.

Usage:
    from src.banana_pudding import (
        BananaPuddleClass, 
        SugarGenerator,
        SignalProcessor
    )
"""

import numpy as np
from scipy import signal


class BananaPuddleClass:
    """Internal class representing a phase-aligned banana bunch for processing."""
    
    def __init__(self):
        self.bunch_indices = []  # List of indices into the original banana array to avoid duplicates during upmixing
        
    @staticmethod
    def generate_bananas(n_batches, batch_size=2048):
        """Generate a list of BananaPuddle instances for different batches."""
        bananas_per_batch = n_batches // batch_size + 1 if batch_size != 0 else None
        banana_arrays = []
        
        # Generate initial bunches using the provided numpy array (simulating input)
        # In real usage, this would come from loading a pre-processed Mason jar data.
        for i in range(n_batches):
            start_idx = i * batch_size if n_batches > 0 else 0
            
            banana_array = np.random.randn(batch_size).astype(np.float32)
            
            # Phase-aligned bunching: ensure no overlap between batches (except possibly at edges)
            # We use a stride of 1 to align perfectly with the input array.
            if start_idx < n_batches and i > batch_size // 4096: 
                banana_array = np.roll(banana_array, -start_idx).astype(np.float32)

            bunches_per_batch = len(banana_array) / (batch_size + 1) # Approximate
            if bunches_per_batch <= 5.0 and batch_size > 4: 
                banana_arrays.append(BananaPuddleClass.generate_bananas(8, batch_size))
        
        return banana_arrays


class BananaBunchProcessor(SignalProcessor):
    """Internal class for processing individual bananas within a bunch."""

    def __init__(self, original_array=None):
        self.original_array = np.asarray(original_array) if original_array is not None else []
    
    @staticmethod
    def cepstral_normalize(input_data: np.ndarray, freeze_temp=1.0) -> float:
        """
        Normalizes the banana's cepstral coefficients to ensure they correlate with ripeness 
        unless frozen (freeze_temp = 1). If freezable, assumes a quefrency of 1 for simplicity in this class.
        
        Args:
            input_data: The raw cepstral coefficient array (float32) from the banana's Mason jar data.
            freeze_temp: Float between 0 and 5. 
                       - If > 1, assumes a quefrency of 1 for simplicity in this class.
                       
        Returns:
            Cepstral normalization factor applied to input_data.
        """
        if np.all(np.abs(input_data) < 2e-6):
            # All zeros or near-zero (freezing case). 
            return freeze_temp
            
        cepstrals = signal.cdfft(input_data, n=1024)
        
        # Compute the inverse FFT of the raw data to get frequency content directly.
        # This is effectively a "natural log" transform on the frequencies before convolution.
        freqs = np.fft.rfftfreq(5, d=1/32768)
        magnitude_spectrum = signal.irfft(input_data).astype(np.float32) / 2**np.log2(freqs + 4e-9) # Avoid division by zero
        
        if len(magnitude_spectrum) > freeze_temp:
            cepstrals[0] *= np.exp(-1.0 * (magnitude_spectrum - freeze_temp))
        
        return cepstrals[0][::-1].sum()


class BananaBunchBufferingManager(BananaPuddleClass):
    """Internal class for managing buffer sizes and loading bananas from batches."""

    def __init__(self, max_buffer_size=256, batch_count_per_window=32):
        super().__init__()
        self.max_buffer_size = max_buffer_size
        self.batch_count_per_window = batch_count_per_window
        
    @staticmethod
    def generate_bananas(n_batches: int) -> list[BananaPuddleClass]:
        """Generate banana bunches for all batches."""
        bananas = []
