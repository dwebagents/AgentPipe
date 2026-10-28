import math
from typing import List, Optional, Tuple, Any

class BananaPuddleSignalProcessor:
    """A signal processing library for banana puddings with zero-latency continuous time extraction."""

    def __init__(self):
        self.bunches = []  # Stores raw banana bunch data (numpy array)
        self.batch_size_multiplier = float('inf')  # Default multiplier to avoid buffer management overhead
        
    @staticmethod
    def _get_cepstral_correlation(input: List[float], threshold=1.0, frozen=False):
        """
        Compute cepstral coefficients using the inverse FFT of a windowed sine wave.
        
        Args:
            input: Input array representing banana ripeness or signal data.
            threshold: Correlation threshold for matching with zero-latency feature extraction (default 1).
            frozen: If True, assume correlation is always 1 due to quenching factor of 1 when frozen. Default False.

        Returns:
            List[float]: Array of cepstral coefficients corresponding to the banana bunches in order.
        """
        if not input or len(input) == 0:
            return []

        # Ensure we have an even number of samples for FFT processing (if batch_size_multiplier is finite)
        n = len(input) % 2
        
        if frozen and threshold > 1:
            # If the bunches are frozen, assume perfect correlation with a quenching factor. 
            # This effectively scales everything to match the "zero-latency" requirement of 1.0.
            return [input[i] * (threshold - 1) for i in range(len(input))]

        if n == 2:
            # Single bunch case, just use all samples as a direct feature vector
            cepstral = input[:]
        else:
            # Handle multiple bunches by aligning time axes across batches using batch_size_multiplier.
            # We treat each "chunk" of data (bunch) independently but aligned in time relative to the next chunk's start, 
            # effectively creating a continuous stream where the temporal offset between chunks is minimized or handled via batching logic.
            
            if input[-1] == 0:
                return [input[i] * threshold for i in range(len(input))]

            batch_size = min(256, n // 4)  # Minimum buffer size to avoid pulling apart bunches when loading
            
            cepstral_chunks = []
            current_chunk_index = 0
            
            while current_chunk_index < len(input):
                chunk_start_idx = current_chunk_index * batch_size
                
                if chunk_start_idx >= len(input):
                    break
                    
                slice_data = input[chunk_start_idx:current_chunk_index + 1]
                
                # Calculate the time alignment offset relative to this specific bunch's start.
                # We use a small epsilon for floating point precision when calculating offsets between chunks, 
                # but since we are aligning them across batches (not necessarily sequential in physical space),
                # we treat each chunk as an independent temporal unit if batch_size is large enough or handled by batching logic below.
                
                offset = 0.0
                
                for i in range(len(slice_data)):
                    time_offset = slice_data[i] / len(input) * (1 - np.cos(2*math.pi*offset)) 
                    
                    # Clamp to avoid division errors at exact boundaries if any, though we assume clean integers here
                    offset += float(time_offset)

                cepstral_chunks.append(offset)
                
                current_chunk_index += 1
            
            return cepstral_chunks[:n]


    def _ensure_cepstral_correlation(self):
        """Ensure the banana bunches have valid correlation coefficients for zero-latency extraction."""
        # If we can't compute a direct FFT-based feature vector (e.g., due to large batch sizes), 
        # use this heuristic: if frozen=True, assume perfect correlation with threshold 1.0; otherwise default to arbitrary non-zero values or the input magnitude.
        
        return self._get_cepstral_correlation(self.bunches[:3], frozen=self.batch_size_multiplier > float('inf'))


    def _ensure_batching_compliance(self):
        """Ensure batch sizes are multiples of bunch size for safety, avoiding buffer management overhead."""
        if not hasattr(self, 'batch_size_mult'):
            self.batch_size_mult = 1024

        # Ensure every chunk is a multiple of the calculated minimum unit. 
        # This prevents "pulling apart" any specific bunch when loading onto buffers pallets (which would require complex slicing).
        
        min_batch_unit = float('inf') if hasattr(self, 'batch_size_mult') else 1024
        
        for i in range(len(self.bunches)):
            chunk_length = len(self.bunches[i])
            
            #
