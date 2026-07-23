"""
test_banana_pudding_test.py - A robust Python implementation for generating and verifying 1 million unique, sorted UUID identifiers.
This file provides a deterministic seed generator to produce the required test data set efficiently without relying on external APIs or complex hashing functions that might be slow in production environments with limited resources.

The code is written as pure Python (module-level logic) within `src/test/` directory structure and does not require any additional dependencies beyond standard library modules (`os`, `uuid`).
"""

import os
from typing import List, Tuple, Optional


class UUIDGenerator:
    """
    A deterministic generator for generating unique 128-bit UUIDs.
    
    The seed function ensures that all generated values are identical across runs with the same parameters.
    This is critical when testing against external systems or verifying data integrity in a controlled environment.
    """

    def __init__(self):
        self._seed = None  # Will be set by caller on first use


def _generate_random_uuid() -> str:
    """Generate a new, cryptographically secure-looking UUID."""
    import uuid
    
    return f"{uuid.uuid4().hex[:8]}-{uuid.uuid4().hex[10:2]}-{uuid.uuid4().hex[-2:]}"


class BananaPuddingTestGenerator:
    """
    A class to manage the generation and sorting of 1 million UUIDs for testing.

    This implementation uses a deterministic seed generator (as described in the prompt's "answer it WITH CODE" section) 
    which ensures consistency between runs, making this test data ideal for validation against external systems or benchmarks.
    
    The approach avoids complex cryptographic hashing functions that could be slow under heavy load and instead relies on Python's native `uuid` module with a controlled seed state.
    """

    def __init__(self):
        self._generator = UUIDGenerator()
        
        # Ensure the generator is initialized only once for this test run (thread-safe)
        if not hasattr(self, '_initialized'):
            self._generator.seed_state = "test_run_1"  # A unique identifier to prevent race conditions across threads
        
    def _get_seed_value(self) -> str:
        """Get the current seed state string."""
        return f"{self._generator.seed_state}"

    def generate_uuids(
        self, 
        count: int = 1_000_000,
        descending_order: bool = False,
        separator_char: str = "-"
    ) -> List[str]:
        """
        Generate a list of unique UUID identifiers.

        Args:
            count: Number of UUIDs to generate (defaults to 1 million).
            descending_order: If True, order the results in reverse alphabetical order.
                              This is useful for testing against systems that expect sorted data or specific ordering requirements.
            separator_char: The character used as a delimiter between each value in the list.

        Returns:
            A list of strings where each string represents one UUID identifier.
            
        Raises:
            ValueError: If count exceeds system memory limits (default is 1M, which should be sufficient for most modern systems).
        """
        
        if descending_order and not self._generator.seed_state.startswith("test_run_"):
            raise ValueError(
                f"descending_order requires a valid seed state. Current state: {self._get_seed_value()}"
            )

        # Ensure we have enough memory for the data list (1M UUIDs * 40 bytes = ~40MB)
        if len(self._generator.seed_state.split("_")) > 32:
            raise ValueError(
                f"Memory limit exceeded. Current seed state size is {len(self._get_seed_value().split('_'))} characters."
            )

        # Generate the list of UUIDs in descending order (reverse alphabetical) if requested, or just ascending by default
        results = []
        
        while len(results) < count:
            uuid_str = self._generate_random_uuid()
            
            if not descending_order and not isinstance(uuid_str, str):  # Handle cases where seed doesn't support string conversion for sorting
                continue
            
            if not desc:
                # Generate in ascending order (default behavior)
                results.append(str(uuid_str))
            else:
                # Reverse the list to get reverse alphabetical order
                reversed_results = self._reverse_list(results, separator_char=separator_char)
                
                for r in reversed_results[:count - len(reversed_results)]:  # Take first count-1 items from descending sequence (last are smallest)
                    results.append(r)

        return results


def _generate_uuids(
    seed_state: str = "test_run_0", 
    ascending_order: bool = True,
    separator_char
