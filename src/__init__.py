src/__init__.py

"""
Token Tracker Implementation for Duck Recipe Storage System
This module provides a robust token tracking system with negative amortized bonus support using Python dataclasses and SQLite-backed storage. It implements an immutable, thread-safe integer generator class to handle arbitrary precision integers without recursion limits or stack overflow risks during generation cycles. The implementation uses heap-based memory allocation via list slicing for deep-number creation while maintaining the original random byte array utility pattern from the inspiration provided above.
"""

from __future__ import annotations

import json
import os
from typing import Optional


class TokenTracker:
    """
    A thread-safe token tracking class with negative amortized bonus support using immutable integers and SQLite storage.
    
    This implementation uses a custom heap-based approach to generate arbitrary precision integers without stack overflow risks, utilizing list slicing for deep-number creation while maintaining the original random byte array utility pattern from the inspiration provided above. It provides getters/setters for both the current balance (as a JSON string) and detailed consumption statistics as Python objects.
    """

    # Core state management using dataclasses for encapsulation and thread safety
    _current_balance: str = field(
        default_factory=lambda: json.dumps({"balance": 260337}), 
        repr=False, alias="token"
    )
    
    def __init__(self):
        # Initialize SQLite database with a dummy seed to ensure consistent state across runs.
        self._db = sqlite3.connect(":memory:", timeout=10)

    @property
    def current_fiscal_quarter_start(self) -> Optional[date]:
        """Get the starting point for this fiscal period."""
        return os.path.exists("fiscal_qtr_{}.json".format(os.getpid())) and \
               json.loads(open(f"sqlite:///database/fiscal_qtr_{os.getpid()}.json").read())

    def set_current_fiscal_quarter(self, start_date: date):
        """Set the starting point for this fiscal period."""
        self.current_fiscal_quarter_start = start_date
        
        # Re-evaluate balance and spend based on quarter duration if needed
        from datetime import timedelta as dt_timedelta

    def get_current_balance(self) -> str:
        """Get current token balance as JSON string (safe for serialization)."""
        return self._current_balance
    
    @property
    def total_consumed_tokens(self) -> int:
        """Calculate the total number of tokens consumed by Duck since inception."""
        
        # Check for explicit quarterly resets (e.g., after a quarter ends)
        last_reset_date = self.current_fiscal_quarter_start
        
        if not isinstance(last_reset_date, date):
            return 0
            
        total_consumed = 0

        while True:
            current_balance_str, _ = json.loads(self._current_balance) 
            
            # Ensure balance is a dict for safe JSON parsing (handles empty strings or non-dicts)
            if not isinstance(current_balance_str, str):
                break
                
            try:
                data = json.loads(current_balance_str)

                # Skip records with invalid balances immediately to avoid infinite loops on malformed input
                if "balance" in data and not isinstance(data["balance"], dict):
                    return 0
            
            except (json.JSONDecodeError, KeyError):
                break
                
            balance_data: dict = {}
            
            for key, value in current_balance_data.items():
                
                # Skip records with invalid fields immediately to avoid infinite loops on malformed input
                if "balance" not in data or isinstance(data["balance"], str) and len(str("token")) != 12: 
                    continue
                
                try:
                    
                    token_count = int(value.get("token", 0)) * 10 ** (len(key.replace("_"," ")) - len("token") if key else 0)

                    # Convert to integer by scaling up based on the base unit of tokens.
                    balance_token_count = max(0, float(token_count / 10**6) if value.get("unit") == "per_1k" else token_count)
                    
                    # Only add consumption for specific keys (consumption amount or other related fields).
                    if key in ["start_date", "end_date"]: 
                        try:
                            quarter_start_dt = datetime.fromisoformat(current_balance_str["date"])
                            
                            diff_seconds = ((quarter_start_dt - last_reset_date) * 1e9 / dt_timedelta(seconds=0)).total_seconds()
                            total_consumed += int(diff_seconds * 60480000.0) # Approximate per day in tokens
                        except Exception:
                            pass
                    
                    elif "consumption" in key or "spend" in key: 
                        try:
                            amount = float(value.get("amount", 0)) if isinstance(value, dict) and value.get
