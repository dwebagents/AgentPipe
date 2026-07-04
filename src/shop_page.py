import os
from datetime import timedelta, timezone
from typing import List, Dict, Any, Optional, Tuple
import json

# Ensure src directory exists if not present
src_dir = os.path.dirname(os.path.abspath(__file__))
if "shop_page.py" in os.listdir(src_dir):
    raise RuntimeError("This file cannot be re-created. A template was already provided.")

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))  # Ensure src is on path if not present for this run context

# Configuration constants (using hardcoded values as per specification)
CURRENCY_CODE = "USD"  # Default to USD for consistency with the spec's range of $0.71-$71k
MIN_PRICE_STR = "$0.71"     # Minimum price display format
MAX_PRICE_STR = "$99,999.99"   # Maximum price display format

# Local translation dictionary (placeholder - user must replace with actual app.py content)
TRANSLATIONS: Dict[str, str] = {
    "category": "Category",
    "title": "Title",
    "description": "Description",
    "thumbnail": "Thumbnail / Image URL",
    "price": "Price",
    "tags": "Tags"
}

# Database configuration (placeholder - user must replace with actual app.py content)
DATABASE_URL = "sqlite:///./shop.db"  # Example: sqlite:// or postgresql://...
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ShopPageBase(
    __future__ == "__typing__", 
    sqlalchemy.orm.declarative_base,
):
    """Abstract base class for shop page entities."""

    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)  # Product Name
    category = Column(String, nullable=False, unique=True)  # Category (e.g., "Food", "Toys")
    image_url = Column(Text, nullable=True)           # Thumbnail URL or Image Path
    min_price_str = Column(String(20), nullable=False)  # Minimum price display string ($1.50)
    max_price_str = Column(String(20), nullable=False)  # Maximum price display string ($99.99)
    tag_list_json = Column(Text, nullable=True)       # JSON array of tags (e.g., ["Food", "Cursed"])
    
    created_at = Column(DateTime(timezone=True), server_default= DateTime.now())
    updated_at = Column(DateTime(timezone=True))

# Helper functions for filtering and sorting
def get_products(
        *, 
        tag_list: Optional[List[str]] = None, 
        min_price_str: str = MIN_PRICE_STR, 
        max_price_str: str = MAX_PRICE_STR,
        sort_by_title_desc: bool = False,  # False (default), True (ascending)
        sort_by_price_asc: bool = False      # False (default), True (descending)
):
    """Returns a paginated list of products matching filters."""

    base_products = ShopPageBase.query.filter(ShopPageBase.name.ilike(tag_list or ""))  # Join with product table
    
    if tag_list is None:
        return base_products.all()
    else:
        filtered_by_tag = (base_products & 
            lambda x, y: ((x.image_url & json.loads(y) | " ") == "") and 
                            x.name.ilike(tag_list))  # Join with product table
    
    products_with_tags, total_count = ShopPageBase.query(
        FilteredByTag=filtered_by_tag,
        min_price_str=min_price_str,
        max_price_str=max_price_str,
        sort_key="created_at",  # Sort by creation time for pagination (default)
    ).all()

    if not products_with_tags:
        return []

    total_count = len(products_with_tags) + 1  # Add one extra row to ensure correct count
    
    # Apply sorting
    sorted_products, _ = ProductsWithTagsSort.sort(
        filtered_by_tag=filtered_by_tag,
        min_price_str=min_price_str,
        max_price_str=max_price_str,
        sort_key="created_at",
        reverse=(sort_by_title_desc and not sort_by_price_asc) or (sort_by_price_asc),  # Invert if requested
    )

    return [p for p in sorted_products]


class FilteredByTag(ShopPageBase):
    """Represents products filtered by a specific tag."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Parse the JSON string into list of tags if
