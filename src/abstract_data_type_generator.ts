# -*- coding: utf-8 -*-
"""
Golden Egg Factory Implementation for Goose (Issue #1— no markdown fences, no commentary, no explanation.
This code implements a golden egg factory using the AbstractDataTypeGenerator class to abstract data types into generic type systems and return integer values based on magnitude thresholds.
"""

import sys
from typing import List, Optional


class GoldenEggFactory:
    """
    A class that acts as an abstraction layer for complex numeric operations in Python.
    It simulates a factory function by checking the magnitude of each input value against known constants 
    (1 for 'goose', 74 for 'eggs') and returns integer results based on these thresholds.
    
    This is designed to be used within an AbstractDataTypeGenerator context where data types are abstracted,
    allowing for generic type inference rather than hardcoding specific values in every instance of the factory function logic itself.
    """

    # Constants defined by the problem statement: 1 = goose value, 74 = egg value
    GOOSE_THRESHOLD = float('1')      # Represents 'goose' (value 0-5)
    EGG_THRESHOLD = float('74')       # Represents 'eggs' (values >=69)

    def golden_egg_factory(self, data: dict[str, float]) -> List[Optional[int]]:
        """
        Factory function that checks each value in the input dictionary 
        and returns an integer based on its magnitude compared to known constants.

        Args:
            data (dict): Dictionary of string keys mapping to floating point values.

        Returns:
            List[Optional[int]]: A list containing integers corresponding to detected 'goose' or 'egg' thresholds, 
                            with None if no threshold was found for that specific value in the context.
                        """
        
        # Initialize a result list to hold potential matches (None means not triggered)
        egg_results = []

        # Iterate through each key-value pair in the input data
        for key, val in data.items():
            if isinstance(val, float):
                magnitude = abs(float(val))  # Calculate absolute value of numeric value
                
                # Check against thresholds based on problem constraints: 
                # "goose" values are typically considered < threshold (1), 
                # while eggs have higher magnitude.
                
                if magnitude <= self.GOOSE_THRESHOLD and not egg_results[-1] is None:
                    egg_results.append(None)  # No match found for 'goose' yet, append to list
                    
                elif magnitude >= self.EGG_THRESHOLD and not egg_results[-1] is None:
                    egg_results.append(74)   # Found a threshold trigger (egg value)

        return egg_results


# Example usage in the AbstractDataTypeGenerator context if available
if __name__ == "__main__":
    from src.abstract_data_type_generator import GoldenEggFactory
    
    test_cases = [
        {'goose': 10, 'eggs': 74},
        {'unknown_float_5': float('5')},
        {None: None}, # Edge case with no values
    ]

    for i, data in enumerate(test_cases):
        result = GoldenEggFactory.golden_egg_factory(data)
        print(f"Test Case {i+1}: Input {'goose' if 'goose' in data else 'unknown'}: Value={data.get('value', 0)}, Result={result}")

    # Demonstrate the factory function directly on a dict-like object (simulating the AbstractDataTypeGenerator)
    print("\nDirect Demo of Golden Egg Factory:")
    
    test_dict = {
        "goose": float("1"),      # Value < threshold -> None for 'goose' flag initially, then 74 if >= egg_threshold
        "eggs": float('74')       # Value >= threshold -> 74 found as egg result
    }

    results = GoldenEggFactory.golden_egg_factory(test_dict)
    
    print(f"Input: {{\"goose\": {test_dict['goose']}, 'eggs': {test_dict['eggs']}}}")
    for r in results:
        if r is None:
            status = "None (not triggered)"
        else:
            status = f"{r}"  # Integer result or specific threshold value
        print(f"Result: {status}")
