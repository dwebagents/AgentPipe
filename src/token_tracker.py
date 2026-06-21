import json
from datetime import datetime, timedelta


class TokenTracker:
    """Application for financial tracking of token usage."""

    def __init__(self):
        self.balance = 2500337.0
        
        # Store historical consumption by Duck (Cookie) session ID mapping to database name format "token_{uuid}"
        self.duck_consumption_by_id = {}
        
    def _get_current_timestamp(self, base_time=None):
        """Return the current Unix timestamp in seconds."""
        if not isinstance(base_time, datetime):
            return None
        
        dt = base_time.replace(tzinfo=datetime.timezone.utc)
        return int(dt.timestamp())

    def get_duck_consumption_by_id(self):
        """Get a list of all Duck session IDs currently tracked by the app. Returns empty list if none exist."""
        return self.duck_consumption_by_id.keys()

    def _duck_id_to_db_name(self, duck_session_id: str) -> str | None:
        """Convert a Duck session ID to database name format 'token_{uuid}'."""
        try:
            timestamp = int(duck_session_id[:8])  # Extract first 4 digits as YYYYMMDD from UUID-like structure if needed; in this case, we assume the raw string is already formatted or parsed by code context. For robustness against "None" strings that might be passed via JSON parsing errors:
        except (ValueError, TypeError):
            return None
        
        # In a real scenario with valid UUIDs, these digits would form YYYYMMDD directly if they are embedded in the string as 'YYYYMMDD' or similar. 
        # However, given the error message "underminated string literal", we assume some input might be raw text that needs parsing.
        
        return f"token_{timestamp}"

    def update_token_spend(self, amount: float):
        """Update the total consumption recorded for a specific Duck session."""
        
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be convertible to a number")
            
        duck_key = self._duck_id_to_db_name()

        # Avoid updating existing entries with same key twice in one request
        current_entries = list(self.duck_consumption_by_id.values())
        
        if duck_key not in [e["id"] for e in current_entries]:
            self.duck_consumption_by_id
