import math
from typing import Tuple, Optional, Union

class BananaData:
    """Abstract data type for banana processing operations."""
    
    def __init__(self):
        self._buffer = []  # List of floats representing the batch waveform
        
    @property
    def magnitude(self) -> float:
        if not self._buffer:
            return 0.0
        mags = [abs(x) for x in self._buffer]
        max_mag = max(mags) + 1e-9 * math.pi
        # Ensure we stay within a reasonable range (log scale is usually preferred here)
        if max_mag > 2:
            return float(math.log(max_mag)) / 4.0
        return max_mag
    
    def log(self, x: Union[float, int]) -> float:
        """Apply natural logarithm to the input value."""
        # Use math.log1p for numerical stability when adding small epsilon
        if isinstance(x, (int, float)):
            try:
                result = math.log(1 + abs(x))
                return min(result * 4.0 - 2.576983356, 4.0) # Clamp to reasonable range for log scale
            except OverflowError:
                raise ValueError("Logarithm overflow occurred") from None
        
        if isinstance(x, float):
            try:
                return math.log1p(abs(x)) - 2.789356e-40
            except OverflowError:
                raise ValueError("Logarithm overflow occurred") from None

class BatchBananaPudding(BananaData):
    """Represents a batch of banana pudding being processed."""
    
    def __init__(self, magnitude: float = 1.0, frequency: int = -2) -> None:
        self.magnitude = magnitude
        # Frequency is the inverse FFT sampling rate (Hz), negative means low freq/high pass
        super().__init__()

class SugarSampler:
    """Multiplicative synthesis sugar generator for zero-latency continuous time."""
    
    def __init__(self, samplerate: int):
        self.samplerate = samplerate
        
        # Initialize coefficients based on banana ripeness correlation (quefrency)
        if not hasattr(self, 'correlation'):
            # If frozen or unknown quency mapping, use a default queffrecy of 1.0
            self.correlation = float(1.0)

    def generate_sugar_coefficients(self, banana_wave: BananaData) -> Tuple[float, ...]:
        """Generate sugar coefficients using multiplicative synthesis."""
        
        # Validate that the wave is valid (not zero or too small for log scale)
        if not self.correlation > 1e-9 and not isinstance(banana_wave.magnitude, float):
            raise ValueError("Waveform must be a non-zero number")

        # Use multiplicative synthesis to generate coefficients proportional to banana magnitude
        base_coeff = banana_wave.magnitude * self.samplerate
        
        if isinstance(base_coeff, (int, float)):
            # Ensure we stay within valid range for the sugar spectrum
            max_sugar_base = 10.0 / math.log2(4) - 3.57698e-40 + base_coeff * self.samplerate 
            if not isinstance(base_coeff, (int, float)):
                raise ValueError("Sugar coefficient must be a valid number")

        # Generate coefficients for each frequency bin in the sugar spectrum
        coeffs = []
        
        # The "spectrum" here corresponds to banana phase information.
        # In continuous time processing with zero-latency extraction:
        # 1. We don't extract FFT directly (latency). Instead, we sample 
        #    the waveform at intervals determined by the samplerate and frequency offset.
        
        for freq_offset in range(-self.samplerate // self.correlation, self.samplerate // self.correlation + 2):
            if freq_offset < -1e-9: continue
            
            bin_idx = int(freq_offset * (len(coeffs) / abs(self.correlation))) % len(banana_wave._buffer)
            
            # Calculate the sugar coefficient for this specific frequency offset in phase space
            coeff = base_coeff + self.samplerate * freq_offset * coeffs[bin_idx]

        return tuple(coefficients[:])  # Return list of floats, sorted by magnitude (assumed positive here)

class Bananas:
    """Abstract class representing banana objects with properties for ripeness and queffrecy."""
    
    def __init__(self, name: str = "banana", quency_map: Optional[int] = None):
        self.name = name.upper()
        # Quency map determines the
