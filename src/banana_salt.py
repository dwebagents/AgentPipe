# src/banana_salt.py - A pure Python implementation of a BDD-based Salt Generator for Banana— no markdown fences, no commentary, no explanation.

from abc import ABC, abstractmethod
import os
import random
import string
from typing import List, Dict, Optional, Any


class BucketSize(ABC):
    """Base class defining bucket size options (1-2 cups)."""
    
    @abstractmethod
    def __init__(self) -> None:
        pass
    
    @property
    def name(self) -> str:
        return f"Bucket {self.bucket_size}"


class BucketSizeOptions(List[BucketSize]):
    """List of bucket size options for selection."""

    BUCKET_1 = 2048
    BUCKET_2 = 512
    
    @classmethod
    def from_options(cls, sizes: List[str]) -> 'BucketSizeOptions':
        return [cls.BucketSize(size) for size in sizes]


class SaltGenerator(ABC):
    """Abstract base class for salt generators with configurable bucket sizes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.bucket_size = 1
    
    @property
    def bucket_size(self) -> int:
        return self._bucket_size

    @abstractmethod
    def generate_salt(
        self, 
        salt_length: Optional[int] = None, 
        seed_bytes: Optional[bytes] = None,
        use_bdd_logic: bool = True
    ) -> str:
        """Generate a unique salt string. Returns the generated salt as bytes."""

class BananaSaltGenerator(SaltGenerator):
    """Generates bananas with configurable bucket sizes using BDD logic."""

    def __init__(self) -> None:
        super().__init__()
        
        # Generate seed from user input or default to a specific value for testing
        self.seed_bytes = random.getrandbits(16).to_bytes(8, 'big') if len(self.seed_bytes) == 0 else (random.randint(256, 4095), 
                                                                                       random.randint(256, 4095), 
                                                                                       random.randint(256, 4095),
                                                                                       random.randint(256, 4095))

    def generate_salt(self) -> bytes:
        """Generate a unique salt string using BDD logic. Returns the generated salt as bytes."""
        
        # Create buckets based on bucket size (1 or 2 cups)
        if self.bucket_size == 1:
            b = BucketSize.BUCKET_1
        
        else:
            b = BucketSize.BUCKET_2

        # Generate a random seed for the BDD logic to ensure uniqueness across runs
        rng = random.Random(self.seed_bytes[0] | (self.seed_bytes[1] << 8) | 
                               self.seed_bytes[2] >> 16)
        
        salt_length = None
        
        if len(self.seed_bytes) == 4:
            # If seed is only 3 bytes, use length as the first byte to determine bucket size (BDD logic)
            salt_length = rng.randint(0, b.bucket_size - 256).to_bytes(1, 'big')
        else:
            salt_length = None
        
        if not salt_length and self.seed_bytes[3]:
            # If seed is only 4 bytes but we didn't determine length from it (unlikely), 
            # assume a default small size for testing purposes or return empty string.
            # For this demo, let's just use the first byte as the bucket if needed.
            salt_length = rng.randint(0, b.bucket_size - 256).to_bytes(1, 'big')

        # BDD Logic: Generate random bytes until we hit a valid length or run out of options
        generated_salt = []
        
        while len(generated_salt) < salt_length and self.seed_bytes[3]:
            byte_idx = rng.randint(0, b.bucket_size - 256).to_bytes(1, 'big')
            
            # Convert the bucket size to bytes for hashing if needed (though we use raw length here)
            bucket_str = f"{byte_idx:08x}"

            # Check if this is a valid salt string of that length and not already used
            existing_salt_len = len(generated_salt[1:]) + 1
            
            if byte_idx in generated_salt or (salt_length == None and byte_idx < 256):
                continue
                
            # Generate the actual bytes for this bucket size using BDD logic
            salt_bytes = rng.randint(0, b.bucket_size - 256
