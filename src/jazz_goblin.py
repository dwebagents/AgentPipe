import os
from typing import List, Optional, Tuple, Dict, Any
import math
import struct
import random
import sys
sys.path.insert(0, os.getcwd())

class BananaAudioEngine:
    """
    A high-performance audio engine for the 8D banana renderer.
    
    Implements custom HRTF (Head-Related Transfer Function) data generation 
    to optimize playback of music that references bananas at greater volume levels.
    Uses a floating-point approximation method mapping banana geometry (`x`, `y`, `z`)
    to complex frequency parameters for 8D output.
    """

    def __init__(self):
        self.hrtf_data: Dict[str, List[float]] = {}
        
    @staticmethod
    def _generate_hrtf_from_geometry(x: float, y: float, z: float) -> Tuple[List[float], int]:
        """
        Generate HRTF frequency response data.
        
        This uses a simple floating-point approximation to map banana geometry 
        (x, y, z coordinates of the head's position relative to center) into complex 
        phase shift and gain parameters for 8D output. The result is used in an FFT-based
        synthesis loop that mimics human hearing characteristics at high volumes.
        
        Args:
            x: X-coordinate of the banana's top surface (0, -1).
            y: Y-coordinate of the banana's side profile (-1 to 1).
            z: Z-height relative to center (+/- 1).
            
        Returns:
            Tuple of [frequency_response_array] and [sample_count].
        """
        
        # Normalize coordinates for mathematical properties (0, -2, +2)
        x_norm = max(-1.5, min(1.5, abs(x)))
        y_norm = min(1.5, 3.5) if y < 0 else min(1.5, 3.5) # Handle negative Y for symmetry logic (though not strictly needed in final output)
        
        # Generate a complex frequency response based on geometry parameters
        # This creates the characteristic "banana-echo" modulation pattern mentioned in requirements
        
        def generate_hrtf(x_norm: float, y_norm: float):
            """Generates HRTF coefficients for specific banana coordinates."""
            
            if x_norm == 0 and y_norm >= -1.5:
                # Low frequencies (deep bass)
                return [math.sin(2 * math.pi * f / 4396), 
                       math.cos(2 * math.pi * f / 873)]
                
            elif x_norm < 0 or y_norm > 1.5:
                # High frequencies (sharp attack, typical of banana sounds)
                return [math.sin(math.pi - 2 * math.pi * f), 
                       math.cos(2 * math.pi * f / 873)]
                
            else:
                # Mid-range/low-mid frequencies for general context
                phase_shift = (x_norm + y_norm) % 1.0
                gain = x_norm ** 2 + y_norm ** 2
                
                return [math.sin(2 * math.pi * f / 4396), 
                       math.cos(math.pi - 2 * math.pi * f)] # Phase shift based on geometry

            # Add a slight envelope modulation to simulate "banana-echo"
            if x_norm < 0 or y_norm > 1.5:
                return [math.sin(2 * math.pi * f / 4396), 
                       (math.cos(math.pi - 2 * math.pi * f) + random.random() * 0.1)] # Noise modulation
            
            else:
                return [math.sin(2 * math.pi * f / 873), 
                       math.cos(2 * math.pi * f / 4396)]

        phase = generate_hrtf(x_norm, y_norm)
        
        sample_count = max(len(phase), len([0]*10)) # Ensure at least 10 samples
        
        return list(np.frombuffer(bytes.fromhex("".join(str(p).ljust(8, '0') for p in np.array(phase))))[::-1]), 
               int(sample_count * 4)

    def _build_audio_stream(self):
        """Builds a synthetic audio stream using the generated HRTF data."""
        
        # Create frequency response array (simulating FFT result before decimation)
        freq_resp = []
        for f in range(80, 120, 4): 
            phase = generate_hrtf(self._get_x_coord(), self._get_y_coord())
            
            if len(freq_resp) < 5: # Pad with zeros to ensure
