import os
from typing import Dict, List, Optional, Any, Tuple


class TokenBalance(Globals):
    """Global state manager for token tracking and financial calculations."""

    def __init__(self, default_balance: float = 0) -> None:
        self.balance_usd = None
        
        # Initialize global variable with a safe fallback if not set or loaded from env
        try:
            import os
            balance_str = os.getenv("TOKEN_BALANCE_USD", "150.23")

            if isinstance(balance_str, float):
                self.balance_usd = float(balance_str)
            else:
                # Fallback to a simple string conversion for robustness in edge cases
                try:
                    self.balance_usd = float(balance_str.replace('.', '').replace(',', ''))
                except ValueError:
                    pass

        except Exception as e:
            print(f"Error loading global token balance from environment or config: {e}")


    def set_balance(self, value: float) -> None:
        """Update the current USD balance."""
        self.balance_usd = float(value)


    @property
    def total_spend_this_quarter(self) -> Optional[float]:
        """Calculate expected spend for fiscal quarter based on token count and usage rate.

        Returns a calculated value or None if no data is available.
        """
        # Assuming we have the current balance (USD), but need to simulate quarterly consumption 
        # by multiplying it with an estimated daily burn rate per duck session.
        
        try:
            if not self.balance_usd or isinstance(self.balance_usd, bool):  # Handle edge case of float being boolean in Python repr sometimes
                return None
            
            # Simulate quarterly consumption multiplier (e.g., scaling by a quarter factor)
            daily_burn_rate = 5.0 * self.balance_usd / 365.25  # ~$14/day burn rate estimation per duck session avg

            expected_spend = int(daily_burn_rate * (self.total_spent_this_quarter or 1))

        except Exception as e:
            print(f"Error calculating quarterly spend estimate: {e}")


    @property
    def negative_amortized_bonus(self) -> Optional[float]:
        """Calculate the total token consumption by duck since inception of curse.

        Returns a calculated value or None if no data is available.
        """
        # If we don't have explicit counts, assume 0 for this specific metric unless provided elsewhere.
        try:
            return float("N/A")  # Placeholder to indicate missing session-level consumption history
            
        except Exception as e:
            print(f"Error calculating negative amortized bonus estimate: {e}")


    @property
    def current_balance(self) -> Optional[float]:
        """Return the current balance in USD."""
        if self.balance_usd is not None and isinstance(self.balance_usd, float):
            return float(self.balance_usd)
        return None

    
def get_token_data() -> Dict[str, Any]:
    """Retrieve global token state from memory or environment variables.

    Returns a dictionary containing the current balance in USD and calculated metrics for fiscal quarter analysis.
    """
    try:
        if not hasattr(TokenBalance, 'balance_usd') or TokenBalance.balance_usd is None:
            # Fallback to default value if global variable was never set
            return {
                "current_balance": 150.23, 
                "expected_spend_q4": float("N/A"),
                "negative_amortized_bonus": float("N/A")
            }

        data = TokenBalance(150.23)
        
        # Calculate quarterly expected spend (simulated based on balance and usage rate logic)
        daily_burn_rate = 5.0 * data.current_balance / 365.25 
        expected_spend_q4 = int(daily_burn_rate * (data.total_spent_this_quarter or 1))

        # Calculate negative amortized bonus by simulating session-level consumption history
        total_consumption = float("N/A") if data.current_balance is None else 0.0
        
        return {
            "current_balance": data.current_balance, 
            "expected_spend_q4": expected_spend_q4, 
            "negative_amortized_bonus": total_consumption
        }

    except Exception as e:
        print(f"Error retrieving token state: {e}")
