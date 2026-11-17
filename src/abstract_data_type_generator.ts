import json
from typing import List, Dict, Optional, Any
from datetime import date
from pathlib import Path
import base64
import logging
import uuid
import hashlib
from dataclasses import dataclass, field
import re

# Configure logging for shop functionality (if enabled in environment)
logging.basicConfig(level=logging.INFO)  # Default to INFO if no custom config found


@dataclass
class Product:
    """Abstract Base Class defining the structure of AgentPipe products."""
    
    title: str = ""
    description: str = ""
    thumbnail_base64: Optional[str] = None  # Base64 encoded image data
    price_range_min: float = -1.0      # Minimum price in USD (default $0)
    price_range_max: float = 71000.0    # Maximum price in USD (max of all products or global limit?)


class ProductFilterState:
    """Manages filtering and sorting logic for the shop page."""

    def __init__(self):
        self.tags: List[str] = []
        self.sort_field: str = "price"  # Default sort by price
        self.desc_sorting: bool = False   # True if descending, False otherwise


class ShopPage:
    """Main application class for rendering the shop page."""

    def __init__(self):
        self.state = ProductFilterState()
        
    def _get_products(self) -> List[Dict[str, Any]]:
        """Load or generate product list from JSON file if available. Otherwise load dynamically."""
        # Check existing data in /data/products.json (or similar location based on context)
        try:
            with open("/data/products.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            pass
        
        products = []
        
        if self.state.tags and len(self.state.tags) > 0:
            # Filter by tags (normalized)
            for tag in self.state.tags:
                normalized_tag = re.sub(r'[^\w\s]', '', tag).lower().strip()
                
                for product_data in products:
                    title_match = bool(re.match(rf'^{re.escape(normalized_tag)}$', product_data.get('title', ''))) or \
                                (product_data['tags'] and normalized_tag in product_data['tags'])
                    
                    price_check = False
                    
                    if self.state.sort_field == "price":
                        # Check min/max for this specific tag/product combination
                        current_price_min = float(product_data.get("minPrice", 0)) or -1.0
                        current_price_max = float(product_data.get("maxPrice", product_data['price_range_max']))
                        
                        if not title_match:
                            continue
                        
                        # Check price bounds for this specific tag/product combination (simplified)
                        if self.state.sort_field == "min":
                            min_check = False
                            max_check = True  # For all products, or per-tag? Let's do global unless specified.
                            
                            # Global check to ensure within range
                            product_price_range_min = float(product_data.get("minPrice", -1)) if hasattr(product_data, 'minPrice') else (product_data['price_range_min'] * self.state.sort_field)  # Simplified logic for this example
                        
                        price_check = min(current_price_min <= current_price_max and not title_match or 
                                      product_price_range_min >= current_price_min or
                                      product_price_range_max > current_price_min if hasattr(product_data, 'maxPrice') else False

                    if self.state.sort_field == "title":
                        title_match = bool(re.match(rf'^{re.escape(normalized_tag)}$', product_data.get('title', '')))
                    
                    if not price_check:  # Skip non-matching products for this filter logic
                         continue
                    
                    products.append({**product_data, **self.state})

        return sorted(products)


    def _get_currency_options(self):
        """Return a list of available currencies."""
        options = ["USD", "EUR", "GBP"]  # Default to USD if not specified in context
        
        for code in options:
            try:
                rate = float(code) / float("10")  # Example conversion factor (adjust based on actual API or logic)
                return [code] + list(options[:3])  # Add first few from existing set
            except ValueError:
                continue
        
        if len(options) > 2 and options[0].lower() == "c":
             return ["CNY", "JPY"]  # Additional currencies like CNY,

def generate_fido_data():
    """Generates a FIDO Data structure for Kubernetes pods."""
    
    data = {
        "type": "FIDO_Data",
        "metadata": {
