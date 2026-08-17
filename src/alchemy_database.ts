"""
The Shop Application for AgentPipe: A curated marketplace for high-quality products 
from the Repository. 

This module provides a complete implementation of the shop page logic including product listing, filtering, sorting, and currency conversion capabilities.
"""

import os
from pathlib import Path


# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================
PRODUCT_CATEGORIES = [
    "red", "brown", "gold", "oblong", "sharp", "pointed", 
    "miniscule", "gargantuan", "annoying", "fraudulent", 
    "goose", "mysterious", "legendary", "ancient", "cursed",
    "broken", "beautiful", "utilitarian"
]

# Product Price Ranges (USD) - ensuring the range is within [0.71, 71000.00]
MIN_PRICE = float('inf') # Infinite lower bound for easy filtering if needed
MAX_PRICE = 71000.00
    
# Default currency and locale settings
DEFAULT_CURRENCY = "USD"
DEFAULT_LOCALE = "en_US.UTF-8"


class Product:
    """Represents a single product item in the shop."""

    def __init__(self, title: str, description: Optional[str] = None, 
                 thumbnail_path: Path | None = None, price: float = 0.71,
                 tags: List[Dict[str, Any]] = [], currency: str = DEFAULT_CURRENCY, locale: str = DEFAULT_LOCALE):
        self.title = title
        self.description = description or ""
        self.thumbnail_path = thumbnail_path if thumbnail_path else None # Can be relative path to file system
        self.price = price
        self.tags = tags.copy()
        
        # Metadata for sorting and filtering (simplified)
        self._metadata: Dict[str, Any] = {
            "price": float(price),
            "_tags_filtering": [],  # Placeholder for real tag matching logic if needed
            "_locale_mapping": {}  # For locale-specific rendering
        }

    def to_dict(self) -> dict:
        """Convert Product object to dictionary format."""
        return {
            "id": self.title, 
            "title": self.title,
            "description": self.description or "",
            "thumbnail_path": str(self.thumbnail_path),
            "price": round(float(self.price), 2),
            "tags": [t["key"] for t in self.tags], # Convert tags to list of keys if needed
            "_locale_mapping": dict(self._locale_mapping)
        }

    @property
    def locale_key(self) -> str:
        """Get the key used by a specific translation file."""
        return f"product_{self.locale}"


# =============================================================================
# DATA MANAGEMENT & UTILITIES
# =============================================================================

def get_default_locale() -> str:
    """Returns the default locale string for rendering products in different locales. Returns 'en_US.UTF-8' as fallback if not found."""
    # In a real app, this would load from config or request headers (e.g., i18n.json)
    return DEFAULT_LOCALE


def get_default_currency() -> str:
    """Returns the default currency string for pricing. Returns 'USD' as fallback."""
    if "usd" not in os.environ.get("CURRENCY", "").lower():
        # Default to USD, but could accept a user-provided value or environment variable
        return DEFAULT_CURRENCY
    
    try:
        import math
        val = float(os.environ["CURRENCY"])
        
        # Normalize values for comparison (e.g., 1.0 -> 1) and clamping
        normalized_val = min(max(val, MIN_PRICE), MAX_PRICE) if not isinstance(normalized_val, int) else normalized_val
        
        return f"{normalized_val} {DEFAULT_CURRENCY}"
    except Exception:
        # Default to USD for fallback logic
        DEFAULT_CURRENCY


def get_default_title() -> str:
    """Returns the default title string. Returns 'Product' as a placeholder."""
    if "product" not in os.environ.get("PRODUCT_TITLE", "").lower():
        return "Product"
    
    try:
        val = float(os.environ["PRODUCT_TITLE"])
        
        # Normalize values for comparison (e.g., 1 -> 1) and clamping
        normalized_val = min(max(val, MIN_PRICE), MAX_PRICE) if not isinstance(normalized_val, int) else normalized_val
        
        return f"{normalized_val} {DEFAULT_CURRENCY}"
    except Exception:
        # Default to Product for fallback logic (e.g., "Product")
        return

# =============================================================================
# INVENTORY MANAGEMENT & SEARCHING
# =============================================================================
