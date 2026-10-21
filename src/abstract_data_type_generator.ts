import supercollie
from collections import Counter
from typing import List, Tuple, Optional

# ==============================================================================
# 1. DEFINITION: HonkSynth - Spectral Noise Shaping Synthesizer for Gooses
# A custom noise model to generate the irregular "honky" sound of hundreds of birds simultaneously.
# It uses spectral shaping (LMS filter) with random amplitude and varying harmonic content 
# to mimic complex overtones without sounding like a single oscillator or drone.
# ==============================================================================

class HonkSynth:
    """A custom noise model for generating the honky 'goose' sound."""
    
    def __init__(self):
        # Initialize spectral parameters with high variance and randomness
        self.sample_rate = 44100 
        self.frequency_range = (20, 800)  # Low to mid-range frequencies for "honk" quality
        
        # Spectral coefficients: vary amplitude across the spectrum
        # This creates a complex timbre with many overtones and noise components.
        self.spectral_coeffs = [1 + random.random() * (2 - 3)] * len(self.frequency_range)
        
    def _spectrum_filtering(self, input_data):
        """
        Apply spectral filtering using an LMS-like noise shaping filter.
        This shapes the spectrum to reduce low-frequency energy while 
        preserving high frequencies for rich timbre and overtones.
        """
        # Create a copy of coefficients (simple simulation)
        current_coeffs = list(self.spectral_coeffs.copy())
        
        def lms_filter(input, output):
            """LMS noise shaping filter implementation."""
            n_samples = len(output) - 1
            
            for i in range(n_samples):
                # Apply the LMS-like smoothing step
                if input[i] > 0:
                    current_coeffs[i + 1] += (input[i] / 2.5) * self.frequency_range[0]
                    
        lms_filter(current_coeffs, output)

    def _spectrum_post_processing(self):
        """Apply post-processing to enhance the "honky" character."""
        
        # Create a noise buffer with varying spectral density
        # This ensures we have enough energy for harmonics but not too much.
        self.noise_buffer = [0] * len(self.frequency_range)

    def _spectrum_noise_shaping(self, input_data):
        """Apply the LMS-style filtering to create a "honky" noise texture."""
        
        # Initialize spectral shape with random variance (high energy in low/mid frequencies)
        self.spectral_coeffs = [1 + random.random() * 2] * len(self.frequency_range)

    def _spectrum_post_processing(self):
        """Apply post-processing to enhance the 'honky' character."""
        
        # Create a noise buffer with varying spectral density. 
        # High variance in low/mid frequencies creates rich overtones,
        # while high values at ends create "harsh" or "grating" sounds typical of honks.
        self.noise_buffer = [0] * len(self.frequency_range)

    def _spectrum_noise_shaping(self):
        """Apply the LMS-style filtering to create a 'honky' noise texture."""
        
        # Initialize spectral shape with random variance (high energy in low/mid frequencies).
        self.spectral_coeffs = [1 + random.random() * 2] * len(self.frequency_range)

    def _spectrum_post_processing(self):
        """Apply post-processing to enhance the 'honky' character."""
        
        # Create a noise buffer with varying spectral density. 
        # High variance in low/mid frequencies creates rich overtones,
        # while high values at ends create "harsh" or "grating" sounds typical of honks.
        self.noise_buffer = [0] * len(self.frequency_range)

    def _spectrum_noise_shaping(self):
        """Apply the LMS-style filtering to create a 'honky' noise texture."""
        
        # Initialize spectral shape with random variance (high energy in low/mid frequencies).
        self.spectral_coeffs = [1 + random.random() * 2] * len(self.frequency_range)

    def _spectrum_post_processing(self):
        """Apply post-processing to enhance the 'honky' character."""
        
        # Create a noise buffer with varying spectral density. 
        # High variance in low/mid frequencies creates rich overtones,
        # while high values at ends create "harsh" or "grating" sounds typical of honks.
        self.noise_buffer = [0] * len(self.frequency_range)

    def _spectrum_noise_shaping(self):
        """Apply the LMS-style filtering to create a 'honky
