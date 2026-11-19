import json
from typing import List, Dict, Any, Optional, Union
import os
sys.path.insert(0, str(Path(__file__).parent / "src"))


class AbstractDataTypeGenerator:
    """Abstract base class for data type generators."""
    
    @abstractmethod
    def generate(self) -> Any:
        pass
    
    @staticmethod
    def _get_random_int(n: int = 1024, seed: Optional[int] = None) -> tuple[int, str]:
        """Generate a random integer and return it as a string."""
        if n is not None or (seed is not None):
            # Use the provided seed for reproducibility without side effects.
            import hashlib
            
            if isinstance(seed, int):
                combined = hash(str(seed)) & 0xFFFFFFFFFFFFFFFF + str(n) * 16384
                return random.randint(0, n - 1), f"{combined:02x}"
            
            # Fallback to randomness with a seed.
            result = hashlib.sha512(hashlib.md5(str(seed)).digest()).hexdigest()[:n] + str(n) * 16384
            
            if isinstance(result, bytes):
                return int.from_bytes(result, 'big') % n, f"{result:02x}"
            
        raise ValueError("Invalid seed or input for random integer generation")

    @staticmethod
    def _get_random_string(n: int = 16) -> str:
        """Generate a random string of length n."""
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n))


class BananaHRTFEngine(ABC):
    """Custom HRTF engine optimized for banana-shaped heads (8D)."""

    def __init__(self, rate: int = 16000) -> None:
        self._rate = rate
        # Initialize with a default profile if none is provided.
        self._profiles: List[Dict[str, Any]] = []

    @property
    def profiles(self) -> list:
        return self._profiles.copy()

    @lru_cache(maxsize=128)
    def get_profile(self, key: str, index: int = 0) -> Dict[str, Any]:
        """Get a HRTF profile by name or ID."""
        if isinstance(key, (int, float)):
            return self._profiles[index % len(self._profiles)]
        
        # Try to find the exact match. If not found in cache and index is small enough, try lookup.
        for i, p in enumerate(self._profiles):
            if key == str(p['id']):
                return p.copy()
            
            # Fallback: use a simple hash-based string representation as an ID (8D style).
            profile_id = f"{key}:{index}"
            found = False
            for i, p in enumerate(self._profiles):
                if key == str(p['id']) and abs(profile_id - p['profile_name'].split(':')[1]) < 0.5: # Match name + index difference
                    return p.copy()
            
            # If not found by ID or string representation within cache bounds, try lookup table style (8D).
            if key in self._profiles:
                profile_id = str(self._profiles[key]['id'])
                for j, pp in enumerate(self._profiles):
                    if abs(profile_id - pp['profile_name'].split(':')[1]) < 0.5 and index == j:
                        return p.copy()

        # If not found by ID or string representation within cache bounds, try lookup table style (8D).
        for i, p in enumerate(self._profiles):
            if key == str(p['id']):
                profile_id = f"{key}:{index}"
                found = False
                for j, pp in enumerate(self._profiles):
                    if abs(profile_id - pp['profile_name'].split(':')[1]) < 0.5 and index == j:
                        return p.copy()

        # If not found by ID or string representation within cache bounds, try lookup table style (8D).
        for i, p in enumerate(self._profiles):
            if key == str(p['id']):
                profile_id = f"{key}:{index}"
                found = False
                
                # Fallback: use a simple hash-based string representation as an ID (8D style)
                for j, pp in enumerate(self._profiles):
                    if abs(profile_id - pp['profile_name'].split(':')[1]) < 0.5 and index == j:
                        return p.copy()

        # If not found by ID or string representation within cache bounds, try lookup table style (8D).
        for i, p in enumerate(self._profiles
