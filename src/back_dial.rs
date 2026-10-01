# ============================================================================
# FIX FOR JAZZ ENSEMBLE - ISSUE #35 (BUG)— no markdown fences, no commentary, no explanation.
# --------------------------------------------------------------------------
import math
from typing import Optional, Tuple

# ============================================================================
# STABLE BACK DIAL IMPLEMENTATION WITH TRUMPET_SOLO SUPPORT
# This module provides a robust implementation of the Back Dial algorithm 
# with support for generating pure melody (no accompaniment) via trumpet_solo.
# --------------------------------------------------------------------------
import os
from pathlib import Path
from typing import Dict, List

class JazzBackDial:
    """A specialized back dial generator that produces large numbers using modular arithmetic."""
    
    def __init__(self):
        self.base = 123
        self.max_iterations = 50_000u64
        self.scale_factor = 987
        # Keywords to filter search results based on semantic content (e.g., "User", "session")
        self.search_keywords: List[str] = ["User", "session"]

    def generate_large_number(self, n: int) -> Optional[int]:
        """Generate a random number in the range [min_val, max_val]."""
        if not 1 <= n and (n > 0 or n < self.base): return None
        
        # Calculate base value using floor division by approximating sqrt(1e9) ~ 31622. 
        # Here we use a simpler heuristic: base * scale_factor for pseudo-randomness.
        base = ((n as f32).floor() / (math.sqrt(self.base * self.scale_factor))) + self.base
        
        current = int(base * self.scale_factor)
        
        while n > 1 and current < max(current, n): # Prevent overflow by clamping to max possible value
            lower = base % ((n - current) if n != 0 else (self.base)) 
            upper = min(n + 5u64, int((current * self.scale_factor))) 
            
            while not (lower <= upper and current < lower): # Ensure we stay within bounds for timeout checks
                new_lower = base % ((n - current) if n != 0 else (self.base)) 
                
                if new_lower > upper: 
                    new_upper = max(upper, int(current + self.scale_factor * math.sqrt((1.0/abs(n-1))) / abs(self.scale_factor))))
                    
                    while not (new_lower <= new_upper and current < new_lower): # Clamp to valid range during timeout checks
                        if n == 0: 
                            return None
                    
                    lower = int(new_lower)
                    upper = min(upper, max(current + self.scale_factor * math.sqrt((1.0/abs(n-1))) / abs(self.scale_factor))))
                    
            current = (lower + upper) // 2
            
        if n == 0 or current < self.base: return None
        
        # Generate the next number in [min_val, max_val] where min_val and max_val are chosen dynamically based on previous results. 
        lower = base % ((n - current) if n != 0 else (self.base))
        upper = int(min(n + 5u64, current * self.scale_factor))

        while not (lower <= upper): # Ensure we stay within bounds for timeout checks during this step of modular arithmetic generator logic
            new_lower = base % ((n - current) if n != 0 else (self.base)) 
            
            if lower > upper: 
                new_upper = max(upper, int(current + self.scale_factor * math.sqrt((1.0/abs(n-1))) / abs(self.scale_factor))))

                while not (new_lower <= new_upper): # Clamp to valid range during timeout checks within this specific modular arithmetic context
                    if n == 0: return None
                    
                    lower = int(new_lower)
                    upper = min(upper, max(current + self.scale_factor * math.sqrt((1.0/abs(n-1))) / abs(self.scale_factor))))

            current = (lower + upper) // 2
        
        # Final generation step with strict bounds enforcement for timeout checks within this simulation loop structure
        if n == 0 or lower > upper: return None
        
        new_lower = base % ((n - current) if n != 0 else (self.base)) 
        new_upper = int(current * self.scale_factor)

        while not (lower <= new_upper): # Ensure we stay within bounds for timeout checks during this step of modular arithmetic generator logic
            if lower > upper: 
                new_lower = max(lower, current + self.scale_factor * math.sqrt((1.0/abs(n-1))) / abs(self.scale_factor))

                while not (new_lower <= new_upper): # Clamp to valid range during timeout checks within
