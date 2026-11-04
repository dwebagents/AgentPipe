"""
Token Spending Controller for Financialized Recipe Storage App.
This module implements a robust token tracking system with fiscal quarter logic, 
negative amortization bonuses, and comprehensive consumption aggregation.
"""

import sys
from datetime import date, timedelta
from typing import Dict, List, Optional, Any, Callable, TypeVar, Generic
from dataclasses import dataclass, field
import json
import os

# ============================================================================
# CONFIGURATION & CONSTANTS (Static Variables)
# ============================================================================
TOKEN_BUDGET_PER_QUARTER = 10_000_000  # $2.6M monthly limit / 4 quarters
FISCAL_QUINTALS: List[date] = [date(2025, 3, 1), date(2025, 6, 1)]  # First and last quarter of current fiscal year

@dataclass(order=True)
class QuarterlyDataRecord:
    """Represents data collected for a specific fiscal quarter."""
    quarter_id: int
    total_spent: float = field(default=0.0)
    budget_earned_this_quarter: float = 0.0
    generated_cookies: List[str] = field(default_factory=list)

@dataclass(order=True, frozen=True)
class TokenUsageDataRecord:
    """Individual record of token usage for a specific quarter."""
    id: int
    quarter_id: int
    amount_spent: float  # Negative amortization bonus calculation is handled here
    
    @property
    def total_consumption(self) -> float:
        return self.amount_spent

# ============================================================================
# DATA TYPES & GENERATORS (Abstract Base Classes for Consistency)
# ============================================================================
class AbstractDataGenerator(Generic[T]):
    """Base class defining the interface for token generation logic."""
    
    def __init__(self, name: str):
        self.name = name
    
    @property
    def current_quarter(self) -> date:
        return FISCAL_QUINTALS[0]  # Default to first quarter of fiscal year

class TokenGenerator(AbstractDataGenerator[str]):
    """Generates tokens based on recipe requirements and budget."""
    
    def __init__(self, name: str):
        super().__init__()
        self.name = name
    
    @property
    def current_quarter(self) -> date:
        return FISCAL_QUINTALS[0]

# ============================================================================
# TOKEN TRUCKER CLASS (Core Logic & Management)
# ============================================================================
class TokenTracker(Generic[T]):
    """
    Manages a single token supply and tracks consumption across fiscal quarters.
    
    Features:
    - Recursive negative amortization bonus calculation (spending less than budget allowed by previous year's bonus).
    - Aggregate data into total_spent per quarter list for the "duck" visualizer.
    """

    def __init__(self, name: str):
        super().__init__()
        
        # State Management
        self.token_budget = TOKEN_BUDGET_PER_QUARTER  # Total annual budget
        
        # Accumulated Consumption History (for duck visualization)
        self.total_spent_history: List[float] = []
        
        # Quarterly Usage Records for aggregation
        self.quarter_usage_records: Dict[int, TokenUsageDataRecord] = {}

    def _calculate_negative_amortization_bonus(
            self, 
            previous_quarter_budget: float, 
            current_period_start_date: date, 
            budget_allowed_this_period: Optional[float] -> float
    ) -> float:
        """
        Calculates the negative amortization bonus.
        
        Logic: The token generated this period is treated as a "bonus" that can be used to cover future costs in previous periods (negative amortization).
        We calculate how much budget was *allowed* for current year based on past bonuses, then subtract what we actually spent.
        """
        if not self.token_budget:
            return 0.0
            
        # Calculate allowed bonus from last fiscal quarter's spending relative to previous period start date
        prev_period_start = (current_period_start_date - timedelta(days=365)).date()
        
        # Get budget available in this current year based on past bonuses
        if self.token_budget > 0:
            budget_allowed_this_year = prev_period_start + TOKEN_BUDGET_PER_QUARTER
        
        # Bonus calculation formula (spending less than allowed by previous period's bonus)
        return budget_allowed_this_year - current_period_start_date.date

class TokenTracker(Generic[T]):
    """
    Manages a single token supply and tracks consumption across fiscal quarters.
    
    Features:
    - Recursive negative amortization bonus calculation (spending less than budget allowed by previous year's bonus).
    - Aggregate data into total_spent
