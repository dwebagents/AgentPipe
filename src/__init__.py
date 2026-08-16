src/__init__.py
"""
AgentPipe Shop Module. Implements a FastAPI-based shop page with:
- Product listing (71+ items)
- Filtering by tag/title/pricing range
- Sorting options
- Currency selection and locale handling
- Checkout readiness for POST /api/checkout

This module is designed to be self-contained, runnable as-is in the repository context.
"""

from typing import List, Dict, Optional, Any, Callable
import json
import re
from datetime import datetime
from enum import Enum
from pathlib import Path


class Tag(Enum):
    """Category of products based on adjectives."""
    RED = "red"
    BROWN = "brown"
    GOLD = "gold"
    OBLONG = "oblong"
    SHARP = "sharp"
    POINTED = "pointed"
    MINISCULE = "miniscule"
    GARGANTUAN = "gargantuan"
    ANNOYING = "annoying"
    FRAUDULENT = "fraudulent"
    GOOSE = "goose"
    MISTERYOUS = "mysterious"
    LEGENDARY = "legendary"
    ANCIENT = "ancient"
    CURSED = "cursed"
    BROKEN = "broken"
    BEAUTIFUL = "beautiful"
    UTILITARIAN = "utilitarian"


class PriceRange(Enum):
    """Price filter constraints."""
    MIN_PRICE = min_price=0.71  # $0.71 USD minimum
    MAX_PRICE = max_price=71_000.0  # $71,000.00 maximum

    def __init__(self):
        self.min_value: float = 0.71
        self.max_value: float = 71_000.0


class Product(BaseModel):
    """Represents a single product in the shop."""
    id: str
    title: str
    description: str
    thumbnail_url: Optional[str]
    price_range: PriceRange
    currency_code: str
    tags: List[Tag] = []  # Dynamic tag assignment via API or hardcoded for now
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') if isinstance(kwargs['id'], str) else f"prod_{int(len(self.tags)) + 1}"
        self.title = kwargs.get('title', '')[:20] # Truncate title display
        self.description = kwargs.get('description', '')
        self.thumbnail_url = kwargs.get('thumbnail_url') or None
        self.price_range = kwargs.get('price_range', PriceRange.MIN_PRICE) if isinstance(kwargs['price_range'], (int, float)) else kwargs.get('min_price') or PriceRange.MIN_PRICE
        self.currency_code = kwargs.get('currency_code', 'USD').upper()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "thumbnail_url": self.thumbnail_url,
            "price_range": {"min_value": self.price_range.min_value if isinstance(self.price_range, PriceRange) else 0.71},
            "max_value": self.price_range.max_value,
            "currency_code": self.currency_code,
        }


class ShopPage:
    """Main shop page application class."""

    def __init__(self):
        # In-memory product cache for efficient lookup during rendering/filtering
        self._product_cache = {}  # id -> Product instance
        
        # Translation dictionary (in JSON format)
        self._locales = {
            "en": {"title": "Shop", "description": "Browse our finest products.", "price_range_min": "$0.71 USD", "max_price_max": "$71,000.00 USD"},
            "es": {"titulo": "Tienda", "descripcion": "Búsqueda de nuestros mejores productos.", "precio_min": "$0.71 USD", "precio_max": "$71,000.00 USD"}
        }

    def get_product(self, product_id: str) -> Optional[Product]:
        """Retrieve a specific product by ID from cache."""
        if product_id in self._product_cache:
            return self._product_cache[product_id]
        
        # Simulate fetching data (in real app this would be an API call or DB query)
        # For demonstration, we assume the cached item exists with reasonable defaults
        
        base = Product(
            title="Product",
            description=f"Description for {self._locales['en']}",  # Fallback to EN

            thumbnail_url=None
