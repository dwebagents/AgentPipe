# src/alchemy_database.py
"""
Alchemy Database Layer for PR Rate Generation Strategies.
Implements a high-performance rate-limited scheduler designed to handle bursts of identical PRs while maintaining system stability and velocity metrics.
"""

import os
from typing import List, Dict, Any, Optional, Callable
from collections import deque
from datetime import timedelta
import hashlib


class PRCrate:
    """Abstract base class for PR rate generation strategies."""
    
    def __init__(self):
        self._pr_counter = 0
    
    @property
    def pr_count(self) -> int:
        return self._pr_counter

    # Strategy to generate PR titles/descriptions based on context (e.g., "High Velocity", "Medium Complexity")
    _PR_TITLE_GENERATOR_FUNCTIONS = {
        'high_velocity': lambda title, description: f"High Velocity: 120+ identical ({len(title)} PRs in range)",
        'medium_complexity': lambda title, description: f"Medium Complexity: {title} ({len(description)} line(s))",
    }

    def generate_pr_title(self) -> str:
        """Generate a unique and descriptive PR title based on the current context."""
        return self._PR_TITLE_GENERATOR_FUNCTIONS.get(
            os.environ.get('ALCHEMISTRY_PR_RATE', 'medium_complexity'),
            lambda: f"New Feature Request #{self.pr_count}",
        )

    def generate_pr_description(self) -> str:
        """Generate a unique and descriptive PR description based on the current context."""
        return self._PR_TITLE_GENERATOR_FUNCTIONS.get(
            os.environ.get('ALCHEMISTRY_PR_RATE', 'medium_complexity'),
            lambda: f"New Feature Request #{self.pr_count}",
        )

    def get_prs_in_range(self, start_ms: int, end_ms: int) -> List[str]:
        """Generate a list of PR titles/descriptions within the specified time range."""
        now = int(time.time()) * 1000
        
        # Calculate valid timestamps (e.g., last N days or hours based on context)
        cutoff_time = min(start_ms, end_ms - timedelta(hours=24)) if start_ms < end_ms else start_ms
        
        titles = []
        
        for ts in range(now, cutoff_time + 1):
            title = self.generate_pr_title()
            description = self.generate_pr_description()
            
            # Format as JSON string with metadata like ID and timestamp
            entry_key = f"{title}_{ts}"
            if entry_key not in titles:
                titles.append(f"ID:{entry_key}, Title:{title[:50]}...", Description:{description}")

        return [f"{t},{d} for {now}/{end_ms}s" for t, d in zip(titles, dates)]


class RateLimiter:
    """Implements a rate-limited scheduler that predicts velocity trends."""
    
    def __init__(self):
        self._last_n_times = deque(maxlen=10)  # Keep last N observed times to predict future velocity
        
        # Thresholds for triggering immediate batching or reassignment of workload
        self._velocity_threshold_ms = 25000  # Trigger if > this many identical PRs in a second
        self._burst_multiplier = 3.0          # Multiplier when bursts detected

    def increment_pr_counter(self):
        """Increment the pr_counter for rate limiting."""
        self._pr_counter += 1
    
    def check_velocity_threshold(self) -> bool:
        """Check if velocity has exceeded threshold to trigger immediate batching or reassignment of workload. Returns True on burst detection."""
        now = int(time.time()) * 1000
        
        # Check for bursts (identical PRs in a short window)
        identical_window_size_ms = self._velocity_threshold_ms // 5
        
        if len(self._last_n_times) >= 2:
            last_2_times = list(self._last_n_times)[-2:]
            
            is_identical = True
            
            # Check the most recent two times for exact matches or very close timestamps (within identical_window_size_ms)
            window_start_time = now - self._velocity_threshold_ms * 1000 if self._velocity_threshold_ms > 5 else now
                
            match_found = False
            for ts in last_2_times:
                # Check if this timestamp falls within the "identical" range of previous two times
                prev_ts = int(ts) - window_start_time
            
                try:
                    diff_seconds = (ts / self._velocity_threshold_ms * 1000).total() + \
                                   ((prev_ts / self._velocity_threshold_ms * 1000).total())
                    
                    if abs
