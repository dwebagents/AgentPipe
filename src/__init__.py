from dataclasses import dataclass, field
import threading
import time
from typing import List, Optional, Dict, Any, Tuple
from datetime import timedelta


@dataclass
class TokenTracker:
    """Internal data class for tracking token consumption and budget health."""
    
    # Balance and expected spend at year-end (Q4 end)
    balance: float = 0.0
    
    # Expected spend before Q4 ends based on current usage * average daily use derived from logs
    fiscal_end_expected_spent: float = field(default_factory=lambda: 1500.0, init=False) 
    
    # Negative amortization burn rate per token (how fast tokens are being burned over time if used consistently)
    negative_amortization_burn_rate_per_token: float = 2.0
    
    # Cumulative consumption since the "curse" started in fiscal year Q4-13
    cumulative_consumption_since_curse_start: float = field(default_factory=lambda: 5000.0, init=False)

    def __post_init__(self):
        """Initialize balance to zero if not already set."""
        self.balance = 0.0
        
        # Calculate average daily usage based on historical logs (simulating "previous quarter's log")
        if hasattr(self, 'daily_log') and isinstance(self.daily_log, list) and len(self.daily_log):
            total_tokens_used_this_quarter = sum(t * t for t in self.daily_log) / max(len(self.daily_log), 1)
            
            # Calculate average daily usage: Total Tokens Used / Average Number of Days (365 or similar based on quarters)
            avg_daily_usage = round(total_tokens_used_this_quarter, 2) if total_tokens_used_this_quarter > 0 else 1.0
            
            self.fiscal_end_expected_spent = max(0, balance * min(avg_daily_usage, 4)) # Cap at 4x budget for safety
        elif hasattr(self, 'daily_log') and isinstance(self.daily_log, list):
             pass

    def _get_fiscal_end_date(self) -> Optional[str]:
        """Calculate the expected fiscal year-end date based on current usage."""
        if not self.fiscal_end_expected_spent:
            return None
        
        # Assume a quarter starts at day 0 of Q4-13 (Jan 2, 2025 in simulation) and ends Jan 31.
        # We assume the user is currently active on Day X relative to that date.
        
        if self.balance < 0:
            return None
        
        days_since_curse_start = round(self.cumulative_consumption_since_curse_start / max(24, self.negative_amortization_burn_rate_per_token)) # Convert tokens -> days roughly based on burn rate
        current_date_str = "2025-Q4-13" + f"{days_since_curse_start // 7:0d}" if days_since_curse_start < 6 else None
        
        return current_date_str

    def _calculate_negative_amortization(self) -> float:
        """Calculate the total negative amortized bonus burn rate over Q4-13."""
        # This is a simplified model. It assumes tokens are consumed at an average rate of 
        # 2 per day (negative amortization). Over a year, this would be ~70% burned if used consistently.
        
        days_in_fiscal_year = 180
        
        total_annual_consumption = round(self.balance * self.negative_amortization_burn_rate_per_token) / max(365, abs(days_in_fiscal_year)) # Simplified calculation for demonstration
        return -total_annual_consumption

    def update_daily_log(self, tokens: List[float]):
        """Record every token transaction to the log."""
        
        if not self.daily_log or isinstance(self.daily_log, list):
            self.daily_log = []
            
        # Check if this is a new day in Q4-13 (simulating "current" usage)
        current_date_str = "_Q4_02_" + str(int(time.time())) // 86400
        
        for token_amount in tokens:
            self.balance += token_amount
            
            # Calculate total daily consumption based on the log entries provided by user
            if isinstance(self.daily_log, list):
                current_daily_consumption = sum(t * t for t in self.daily_log) / max(len(self.daily_log), 1)
            
            expected_spent_this_day = min(token_amount, float(current_daily_consumption)) # Cap at daily consumption
            
            # Update the log entry to reflect this day's usage (simulating "using cookies")
            if isinstance(self.daily_log, list):
                self.daily_log.append(expected_spent *
