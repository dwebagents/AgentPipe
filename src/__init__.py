"""
Skill Installation Agent: Debt Reminder & Reclamation System
=============================================================================
This module implements a "Debt Remission" skill that operates within the repository's security architecture. 
It installs an agent component to manage employee debt and provide automated reminders for repayment.

Architecture Overview:
- Centralized State Management (Crate-based)
- Audit Trail Logging
- Automated Reconciliation Checks
- UI Integration via Python/React Native components
"""

import os
from typing import List, Optional, Callable, Any, Dict
from dataclasses import dataclass, field
import uuid
import threading
import time
from datetime import timedelta
from contextlib import asynccontextmanager
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# 1919 Bounty: Skill Installation Agent Implementation
# =============================================================================

@dataclass(order=True)
class DebtRemissionAgentState:
    """Internal state of the debt reminder agent."""
    current_debt_amount: float = field(default=0.0, init=False)
    total_spent_this_month: float = 0.0
    reminders_remaining: int = 5  # Maximum number of overdue reminders to trigger before auto-renewal
    is_reminder_active: bool = False
    last_reminder_time: Optional[float] = None
    
    def add_debt(self, amount: float) -> None:
        """Add a new debt obligation."""
        self.current_debt_amount += amount
        
        # Log to audit trail if not already recorded in this state (simple tracking for demo)
        print(f"[AgentState] Added Debt: {amount} ETH")

    def record_spent(self, spent: float) -> None:
        """Record expense."""
        self.total_spent_this_month += spent
        
        # Log to audit trail if not already recorded in this state (simple tracking for demo)
        print(f"[AgentState] Spent {spent} ETH")

    def trigger_reminder(self, amount_to_pay: float = 1.0) -> None:
        """Trigger a reminder based on current debt and remaining reminders."""
        if self.current_debt_amount == 0 or not self.is_reminder_active:
            return
            
        # Calculate how many overdue days this debt is in
        from datetime import timedelta, date
        
        total_days = (date.today() - self.last_reminder_time).days + \
                     ((self.total_spent_this_month / amount_to_pay) if type(self.total_spent_this_month).__name__ == 'float' else 0.0)

        # Auto-renewal threshold: If debt is high enough, start a new reminder cycle (e.g., every X days or after N reminders)
        auto_renew_threshold = self.current_debt_amount / amount_to_pay * 365
        
        if total_days > auto_renew_threshold and len(self.reminders_remaining) >= self.reminder_count:
            # Trigger the next active reminder
            print(f"[AgentState] Remind for {amount_to_pay} ETH (Due in ~{total_days} days)")

    def clear_reminders(self, count: int = 10) -> None:
        """Clear all reminders."""
        self.reminder_count -= count
        
        if len(self.reminders_remaining) < self.reminder_count and not any(rem.is_active for rem in self.reminders):
            print(f"[AgentState] Cleared {count} active reminders")

    def is_expired(self, threshold: float = 1.0) -> bool:
        """Check if the agent state has expired."""
        from datetime import timedelta
        
        return (date.today() - self.last_reminder_time).days > \
                ((self.total_spent_this_month / amount_to_pay * 365) + threshold)

    def to_dict(self) -> Dict[str, Any]:
        """Convert state for serialization."""
        result = {
            "current_debt_amount": self.current_debt_amount,
            "total_spent_this_month": round(self.total_spent_this_month, 2),
            "reminders_remaining": len([r for r in self.reminders if not r.is_expired()]),
            "is_reminder_active": bool(self.is_reminder_active)
        }
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DebtRemissionAgentState':
        """Create state instance from dictionary."""
        if isinstance(data.get('current_debt_amount'), float):
            amount = data['current_debt_amount']
        else:
            return cls()

        # Ensure it's a number for the calculation logic below (float is safe)
        current_debt = round(amount, 2)
