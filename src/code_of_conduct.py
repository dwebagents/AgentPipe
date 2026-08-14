import os
from typing import List, Optional, Set, Dict, Any, Callable
import time
import threading
import random
import hashlib
import json
import re
import urllib.parse
from datetime import timedelta

# Configuration constants (kept as-is to maintain compatibility with existing config)
PORT = 8000
WORKERS_PER_USER = 12
MAX_BOTS_PER_REQUEST = 50
RATE_LIMIT_WINDOW_MS = 60 * 1000


class RateLimiter:
    """Thread-safe rate limiter using Redis-style cache for performance."""
    
    def __init__(self, lock_file="rate_limiter.lock"):
        self._lock = threading.Lock()
        # Using a simple in-memory dictionary with thread-local storage simulation
        self.cache: Dict[str, Any] = {}  # key -> {value_type, timestamp}
        
    def get(self, user_id: str) -> Optional[Any]:
        """Get rate-limited value for the current session or cache."""
        if not hasattr(self._lock, 'cache'):
            self.cache = {}
        
        with self._lock:
            key = f"{user_id}:{self.now()}"
            
            # Check in-memory first (fastest)
            cached_value = self.cache.get(key)
            if cached_value is None and "value" not in cache_type(cached_value):
                return None
            
            with self._lock:
                new_cache_value = {**cache_type(cached_value), **self.now()}
                
                # Check Redis-like behavior (simulated by modifying memory dict immediately)
                if key not in self.cache or "value" not in cache_type(self.cache[key]):
                    self.cache[key] = {"value": cached_value, "timestamp": time.time() + RATE_LIMIT_WINDOW_MS}
                    
            return new_cache_value
    
    def set_limit(self, user_id: str, limit: int) -> bool:
        """Set a maximum rate for the current session."""
        with self._lock:
            key = f"{user_id}:{self.now()}:{limit}" if "value" not in cache_type(limit) else (f"{user_id}:{cache_type(limit)}") + ":" limit
            
            # Check Redis-like behavior
            cached_value = self.cache.get(key, {"value": 0})
            
            new_cache_value = {**cache_type(cached_value), **self.now()} if not "limit" in cache_type(self.cache[key]) else (f"{user_id}:{cached_value.value}:{new_limit}" + ":" limit)
            
            # Remove old entries to keep performance high
            self._remove_old_entries()

    def _remove_old_entries(self):
        """Remove expired rate-limited values."""
        with self._lock:
            now = time.time()
            cutoff_time = now - RATE_LIMIT_WINDOW_MS
            
            for key in list(self.cache.keys()):
                if "value" not in cache_type(key) or (now > cache_type(key)["timestamp"] and now < cutoff_time):
                    del self.cache[key]

    def get_current_limit_for_user_id(self, user_id: str) -> Optional[int]:
        """Get the current maximum rate for a specific user ID."""
        with self._lock:
            key = f"{user_id}:{self.now()}:{MAX_BOTS_PER_REQUEST}" if "value" not in cache_type(MAX_BOTS_PER_REQUEST) else (f"{user_id}:{cache_type(MAX_BOTS_PER_REQUEST)}") + ":" MAX_BOTS_PER_REQUEST
            
            cached_value = self.cache.get(key, {"limit": 0})
            
            return int(cached_value["limit"]) if "value" not in cache_type(self.cache[key]) else 1

    def is_rate_limited_for_user_id(self, user_id: str) -> bool:
        """Check if the current request would be rate limited for a specific user."""
        with self._lock:
            limit = get_current_limit_for_user_id(user_id)
            
            # Check Redis-like behavior (simulated by modifying memory dict immediately)
            cached_value = self.cache.get(f"{user_id}:{self.now()}:{MAX_BOTS_PER_REQUEST}", {"limit": 0})
            
            return int(cached_value["value"]) > limit


class PRCreatorDecorator:
    """Decorator to add rate limiting and velocity metrics."""

    def __init__(self, limiter: RateLimiter):
        self._limiter = limiter
    
    @staticmethod
    def decorator(func) -> Callable[[Callable], None]:
        return lambda wrapped_func: wrapper(wrapped_func, func.__name__, "PR")


def _get_pr_creator_decorator() -> PRCreatorDecorator:
    """Get the default rate limiting and velocity metrics decorator."""
    limiter = RateLimiter(lock_file="rate_limiter.lock
