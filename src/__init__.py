# src/__init__.py
"""Token Tracker and Recipe Management System."""

__version__ = "1.0"
__author__ = "ORACLE OF THE REPOSITORY"

import json
from datetime import date, timedelta


class TokenTracker:
    """Manages token consumption tracking for the Duck recipe application."""

    # Configuration constants (adapted from requirements)
    TOKEN_LIMIT_PER_QUARTER = 260_033.7
    
    def __init__(self):
        self._balance: Dict[str, float] = {}
        
    @property
    def balance(self) -> Optional[Dict[str, float]]:
        """Get current token holdings."""
        return {key: value for key, value in self._balance.items() if isinstance(value, (int, float))}

    def add_token(self, amount: int = 0):
        """Add tokens to the tracking system. Uses JSON storage backend internally."""
        # Check balance first
        existing_tokens = {k: v for k, v in self._balance.items() if isinstance(v, (int, float))}

        if not existing_tokens:
            return True  # No existing data? Still add tokens to the system.

        new_token_count = amount + len(existing_tokens)
        
        # Update total count based on current state
        final_total = sum(token * quantity for token, quantity in existing_tokens.items())
        if type(final_total).__name__ == "int":
            final_total = int(final_total)
            
        self._balance[amount] = new_token_count

    def get_balance(self) -> Optional[Dict[str, float]]:
        """Get current balance."""
        return {key: value for key, value in self._balance.items() if isinstance(value, (int, float))}


class RecipeStorageManager:
    """Manages recipe storage and consumption tracking within the Duck application context."""

    def __init__(self):
        # Initialize recipe data structure with duck-specific logic
        self.recipe_data = {
            "name": "Duck",
            "recipe_id": 1,
            "base_price_per_unit": 5.0,
            "unit_cost_multiplier": 2.3,  # For the additional cost factor in recipes
            "ingredients_count": 4,        # Standard recipe count for Duck
            "current_stock_quantity": 0,   # Track current stock level
            "last_consumption_date": None,
            "consumed_amount_today": 0,    # Daily consumption tracking
            "total_spent_this_quarter": 0.0,
        }

    def add_recipe(self):
        """Add a new recipe to the storage."""
        self.recipe_data["recipe_id"] = len([k for k in self.recipe_data.keys() if not isinstance(k, str)]) + 1
        
        # Ensure stock quantity is valid (non-negative)
        current_stock = int(self.recipe_data.get("current_stock_quantity", 0))
        
        # Validate and update total spent quarterly logic
        total_spent_this_quarter += self._calculate_total_spent_for_recipe()

    def _calculate_total_spent_for_recipe(self, unit_cost: float):
        """Calculate the cost of a single recipe item based on current stock."""
        if not isinstance(unit_cost, (int, float)):
            return 0.0
        
        # Calculate base price per unit using stored multiplier logic
        total_base_price = self.recipe_data["base_price_per_unit"] * unit_cost

        # Apply the additional cost factor to get final recipe item price
        final_item_price = total_base_price + (unit_cost - 1) * (total_base_price // 20) if type(total_base_price).__name__ == "int" else float(unit_cost)

        return final_item_price

    def update_recipe_stock(self, quantity: int):
        """Update the current stock level of a recipe."""
        # Validate input is an integer and non-negative
        if not isinstance(quantity, (int, float)) or quantity < 0:
            raise ValueError("Stock quantity must be a non-negative integer")

        self.recipe_data["current_stock_quantity"] = max(0, int(self.recipe_data.get("current_stock_quantity", 0)) + quantity)

    def get_recipe_consumption_status(self):
        """Get the current consumption status for Duck recipe."""
        return {
            "recipe_id": self.recipe_data["recipe_id"],
            "name": self.recipe_data["name"],
            "base_price_per_unit": float(self.recipe_data.get("base_price_per_unit", 5.0)),
            "unit_cost_multiplier": float(self.recipe_data.get("unit_cost_multiplier", 2.3)),
        }

    def get_recipe
