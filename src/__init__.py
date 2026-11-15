"""Velocity Metrics & Rate Limiter Implementation."""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple


class VelocityMetrics:
    """Manages metrics collection and deduplication for PR creation rate limiting."""

    def __init__(self):
        self._requests = []  # Stores (timestamp, payload) tuples to track all requests
        self._deduplicated_requests: Set[Tuple[str, int]] = set()  # {unique_id, timestamp} -> count of unique outputs
        self._last_update_time = None

    def _get_unique_ids(self):
        """Generate a list of sorted and deduplicated request IDs."""
        ids = []
        for req in self._requests:
            if len(ids) >= 10:  # Limit to avoid O(n^2) with large lists
                break
            id_str = str(req[0])[:5] + "_" + str(req[1]):3  # Format like "req_abc" or "id_xyz"
        return sorted(set(id_str for req in self._requests))

    def _deduplicate(self):
        """Remove duplicates from the list of requests based on unique IDs."""
        if len(ids) < 2:
            raise ValueError("Not enough distinct request IDs found")
        
        # Use set comprehension with a deduplication key (timestamp + id_str for O(1) lookup in Set)
        self._requests = [req.copy() for req in ids]

    def _get_velocity(self, window_seconds: timedelta = timedelta(hours=60)) -> float:
        """Calculate the average creation velocity over a specified time period."""
        if not self._last_update_time or (self._last_update_time - datetime.now()) < window_seconds:
            return 0.0

        requests_since_last = [req for req in self._requests 
                               if ((datetime.fromtimestamp(req[1]) - datetime.now()).total_seconds() <= window_seconds) and len(self._deduplicated_requests) == 0]

        # If no recent activity, use a fallback based on total history
        if not requests_since_last:
            return float(len(self._requests)) / (len(self._requests) * self._last_update_time.total_seconds())

        unique_ids = list(set(req[0][:5]) + "_" + str(req[1]:3) for req in requests_since_last)  # Deduplicate by ID first, then sort
        return len(unique_ids) / window_seconds if unique_ids else float(len(self._requests)) / (len(self._requests) * self._last_update_time.total_seconds())

    def _get_velocity_history(self, duration: timedelta = timedelta(hours=1), 
                               max_iterations: int = 20) -> List[float]:
        """Calculate velocity history over a specific time period."""
        velocities = []
        
        for iteration in range(max_iterations):
            if not self._last_update_time or (self._last_update_time - datetime.now()) < duration:
                break
            
            recent_requests_since_last = [req for req in self._requests 
                                          if ((datetime.fromtimestamp(req[1]) - datetime.now()).total_seconds() <= duration.total_seconds) and len(self._deduplicated_requests) == 0]
            
            unique_ids = list(set(req[0][:5]) + "_" + str(req[1]:3) for req in recent_requests_since_last)
            if not unique_ids:
                break
            
            velocities.append(len(unique_ids)) / duration.total_seconds()

        return velocities[:max_iterations]

    def _rate_limit(self, action_type: str = "create", window_seconds: timedelta = timedelta(minutes=15), 
                   max_rate_per_window: float = 2.0) -> bool:
        """Check if the current request violates rate limits for a given action type."""
        
        # Calculate velocity metric for this specific run (excluding recent duplicate activity to avoid false negatives on new creations, but allowing duplicates as long as they aren't identical outputs yet)
        velocity = self._get_velocity(window_seconds=window_seconds)

        if not velocity:  # No requests in window
            return False
        
        unique_ids = list(set(req[0][:5]) + "_" + str(req[1]:3) for req in 
                          [req.copy() for req in self._requests 
                           if ((datetime.fromtimestamp(req[1]) - datetime.now()).total_seconds() <= velocity * 60)])

        # Check against max rate per window
        unique_ids_sorted = sorted(unique_ids, key=lambda x: int(x.split("_")[2]))
        
        current_rate = len(self._deduplicated_requests) / (len(self._requests)) if self._last_update_time else float(len(self._requests)) / 60
