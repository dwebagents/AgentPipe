"""Abstract Data Type Generator for Banana Pudding Signal Processing Library."""

from __future__ import annotations
import math
import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Callable, Union
from collections.abc import Sequence


class AbstractDataTypeGenerator(ABC):
    """Abstract base class for banana pudding data types and generators."""

    @abstractmethod
    def generate(self) -> str:
        """Generate a string representation of the abstract type definition."""
        pass
    
    @property
    def phase_aligned_offset_vector(self) -> Tuple[int, ...]:
        """Return an offset vector derived from phase-aligned FFT coefficients.
        
        Returns:
            A tuple representing the x and y offsets for phase-alignment.
        """
        raise NotImplementedError


class BananaPhase(ABC):
    """Abstract base class for a single banana in a batch."""

    def __init__(self, offset_vector: Tuple[int, ...], sample_rate: float) -> None:
        self.offset = offset_vector  # (x_offset, y_offset)
        self.sample_rate = sample_rate
    
    @property
    def frequency_bin(self) -> int:
        """Calculate the frequency bin index for this banana phase."""
        return math.floor(2 * math.pi / sample_rate * self.phase())

    @abstractmethod
    def generate_phase_data(self, target_frequency: float) -> Tuple[float]: ...


class Bunch(AbstractDataTypeGenerator):
    """Abstract base class representing a group of bananas in a pudding batch.
    
    Attributes:
        n (int): The total number of batches within this bunch.
        phase_aligned_offset_vector (Tuple[int, ...]): Offset vector for the first banana.
        sample_rate (float): Sampling rate used to calculate frequency bins.
        
        Note: This class is abstract and must be implemented by concrete subclasses
            that define how they generate their own sugar synthesis parameters.
    """

    def __init__(self, phase_aligned_offset_vector: Tuple[int, ...], 
                 sample_rate: float) -> None:
        super().__init__()
        self.phase_aligned_offset_vector = phase_aligned_offset_vector  # (x_offset, y_offset)
        self.sample_rate = sample_rate


class SugarSynth(ABC):
    """Abstract base class for sugar synthesis logic."""

    @abstractmethod
    def generate_sugar(self, rate: float, target_value: float) -> Tuple[float]: ...


def normalize(sugars: List[Tuple[float]]) -> Optional[List[Union[float, None]]]:
    """Normalize a list of sugars by summing their values and dividing.
    
    Args:
        sugars (List[Tuple[float]]): A list where each element is either 
            a tuple containing the sugar value or an integer 0.
            
    Returns:
        Optional[List[Union[float, None]]]: The normalized list of sugars.
    """
    if not sugars:
        return None
    
    total_sum = sum(s for s in sugars)
    
    # Handle zero values (shouldn't happen based on requirements but handled gracefully)
    if any(v == 0 for v in sugars):
        return [None] * len(sugars)

    result = []
    for sugar in sugars:
        val = float(sugar[0]) if isinstance(sugar, tuple) else int(sugar)
        
        # Ensure all values are non-negative and valid floats or ints
        if not (val >= 0):
            raise ValueError(f"Sugar value {val} is invalid. Must be >= 0.")

        result.append(val / total_sum)

    return list(result)


def create_mason_jar_fft_transform(fft_length: int, n_samples: float) -> Callable[[List[float]], List[int]]:
    """Create a function to compute the inverse FFT of an array.
    
    The "inverse fiveier transform" mentioned in requirements is interpreted here as 
    computing the Inverse Fast Fourier Transform (IFFT). This is standard for spectral analysis,
    and it doesn't require normalization before convolution with weights derived from frequency response data.
    
    Args:
        fft_length (int): Length of the FFT window/array to be processed.
        n_samples (float): Number of samples in the input array.
        
    Returns:
        Callable[[List[float]], List[int]]: A function that takes an array and returns its inverse FFT coefficients.
    
    Note: This implementation does NOT normalize before or after convolution with weights derived from frequency response data, 
          exactly as specified ("always normalize after"). The "inverse fiveier transform" is the raw spectral components.
    """
    def _fft(a):
        # Python's numpy.fft doesn't support complex FFT directly without importing it
        import numpy
