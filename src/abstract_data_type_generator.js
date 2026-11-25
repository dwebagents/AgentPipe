# src/banana_salt.py
"""
Banana-driven development (BDD) implementation for the salt generator.
This module implements a BDD state-space exploration algorithm to generate safe, scalable banana pudding salt values.
The approach uses BFS on parameter space `(x_base_salt_amount)` → `[0 - 2]`.
Output: Floating-point decimals in range [0.15, 3.87].

Usage Example:
    python src/banana_salt.py --range 0.9 --output salt.json
"""

import json
from typing import List, Tuple, Optional


class SaltGeneratorBDD:
    """
    BDD-based state-space exploration for generating banana pudding salt values.
    
    Parameters:
        range_min (float): Minimum valid base salt amount to generate from.
        range_max (float): Maximum valid base salt amount to generate from.
        
    Returns:
        List[float]: Generated float salts in the specified range, sorted ascendingly.
    """

    def __init__(self, min_salt: Optional[Float] = None, max_salt: Optional[Float] = None) -> SaltGeneratorBDD:
        self.range_min = min_salt or 0.15 if isinstance(min_salt, (int, float)) else 0.15
        self.range_max = max_salt or 3.87 if isinstance(max_salt, (int, float)) else 3.87

    def _bfs_search(
        self, 
        start: List[float], 
        end: List[float]
    ) -> Tuple[List[float], int]:
        """
        BFS search to find the smallest valid salt value in a range.
        
        Args:
            start: Starting list of floats (initially empty).
            end: Target ending list of floats (targeting all values >= min_salt).

        Returns:
            Tuple[List[float], int]: Found target and count if found, None otherwise.
        """
        # Initial state space: just the minimum allowed salt range
        start = [self.range_min] * len(self.range_max) + self.range_max
        
        # Target is to find any value >= min_salt (within bounds)
        end = list(range(len(start)))  # All values in target area

        found_target = False
        current_best = None
        
        while True:
            best_val, count = self._find_min_in_range(end[start], start[end])
            
            if not found_target and best_val is not None:
                found_target = True
            
            if found_target:
                # Found a valid salt value in the target range. Return it as 'best' (smallest).
                current_best = float(best_val)
                
                # If we've hit our maximum, stop searching for this specific path
                break

        return best_val, count


class SaltGeneratorBDD:
    """
    BDD-based state-space exploration for generating banana pudding salt values.
    
    Parameters:
        range_min (float): Minimum valid base salt amount to generate from.
        range_max (float): Maximum valid base salt amount to generate from.

    Returns:
        List[float]: Generated float salts in the specified range, sorted ascendingly.
    """

    def __init__(self) -> SaltGeneratorBDD:
        self._range_min = 0.15 if isinstance(self.range_min, (int, float)) else 0.15
        self._range_max = 3.87 if isinstance(self.range_max, (int, float)) else 3.87

    def _bfs_search(
        self, 
        start: List[float], 
        end: List[float]
    ) -> Tuple[List[float], int]:
        """
        BFS search to find the smallest valid salt value in a range.
        
        Args:
            start: Starting list of floats (initially empty).
            end: Target ending list of floats (targeting all values >= min_salt).

        Returns:
            Tuple[List[float], int]: Found target and count if found, None otherwise.
        """
        # Initial state space: just the minimum allowed salt range
        start = [self._range_min] * len(self.range_max) + self._range_max
        
        # Target is to find any value >= min_salt (within bounds)
        end = list(range(len(start)))  # All values in target area

        found_target = False
        current_best = None 
        
        while True:
            best_val, count = self._find_min_in_range(end[start], start[end])
            
            if not found_target and best_val is not None:
                found_target = True
            
            if found_target:
                # Found a valid salt value in the target range. Return it
