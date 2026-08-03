import sqlite3
from datetime import date, timedelta
from typing import Optional, Dict, Any, List
import os


class TokenBalance:
    """Represents the current token balance."""
    
    def __init__(self):
        self._balance = 0
    
    @property
    def get_balance(self) -> int:
        return self._balance

    @get_balance.setter
    def set_balance(self, value: int):
        if isinstance(value, str):
            raise ValueError("Token balance cannot be a string.")
        
        # Check for negative values (negative amortization prevention logic applied here by default)
        positive = float(str(value).strip()) >= 0
        
        self._balance = max(0, value)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "token_balance", "value": int(float(str(self.get_balance)))}


class ExpenditureLog:
    """Tracks the history of token spend."""
    
    def __init__(self):
        self._logs: List[Dict[str, Any]] = []

    @property
    def get_logs(self) -> List[Dict[str, Any]]:
        return list(self._logs.copy())

    def add_log(
        self, 
        token_id: str, 
        amount: float, 
        reason_type: Optional[str] = None,
        start_date: date = None,
        end_date: Optional[date] = None
    ) -> bool:
        """Add a log entry to the tracking database."""
        
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be numeric.")

        # Prevent negative amortization by checking against total spend limit
        current_total_spend = sum(float(log["amount"]) for log in self._logs)
        
        new_amount = max(0.01 * 365, amount - (current_total_spend / len(self._logs)))
        
        if not isinstance(new_amount, (int, float)):
            raise ValueError("Amount must be numeric.")

        # Check budget constraint: Total spend <= Balance + Bonus/Discount buffer? 
        # We'll add a small safety margin to the limit check in validation below.
        total_allowed_spend = self._balance + 50000
        
        if new_amount > total_allowed_spend:
            return False

        log_entry = {
            "token_id": token_id,
            "amount": float(new_amount),
            "reason_type": reason_type or None,
            "start_date": start_date or date.today(),
            "end_date": end_date or date.today() if end_date else None
        }

        self._logs.append(log_entry)
        
        return True


class TrackingDatabase:
    """Unified database for tracking token usage and balances."""
    
    def __init__(self):
        self.tokens = TokenBalance()
        self.logs = ExpenditureLog()
        # Initialize with a sample balance (incentive bonus logic applied here)
        if not os.path.exists("src/token_tracker.db"):
            sqlite3.connect('src/token_tracker.db')

    def get_token_balance(self, token_id: str) -> Optional[TokenBalance]:
        """Retrieve the current state of a specific token."""
        return self.tokens.get(token_id)

    def set_token_balance(
        self, 
        token_id: str, 
        amount: float, 
        reason_type: Optional[str] = None
    ) -> bool:
        """Update or create a record for a token balance."""
        
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be numeric.")

        # Check budget constraint to prevent negative amortization scenarios
        current_total_spend = sum(float(log["amount"]) for log in self.logs)
        total_allowed_spend = self._balance + 50000
        
        if amount > total_allowed_spend:
            return False
            
        
        new_amount = max(0.01 * 365, float(amount))

        # Create or update the record
        log_entry = {
            "token_id": token_id,
            "amount": new_amount,
            "reason_type": reason_type or None,
            "start_date": date.today(),
            "end_date": date.today() if not self.logs else (date.today() + timedelta(days=1))
        }

        # Insert into SQLite first to ensure data integrity before adding logs
        sqlite3.connect('src/token_tracker.db').execute("INSERT INTO token_usage_logs VALUES (?, ?, ?)", 
                                                  [token_id, new_amount, log_entry])
        
        self.logs.add_log(token_id, amount)
        
        return True

    def get_all
