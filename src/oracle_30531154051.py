"""
The Oracle of the Repository: A Data Loader and Frontend Template Generator
This file implements a robust data loader to fetch product listings from an external API or mock database. It supports JSON/YAML/CSV formats for structured mappings and generates HTML templates for rendering products on `/shop`.
"""

import json
from typing import List, Dict, Optional, Any, Union
from pathlib import Path
import os
import re


# ============================================================================
# DATA LOADER MODULE: Product Data
# A robust data loader that handles JSON/YAML/CSV mappings of AgentPipe product details.
# It supports filtering by tag, title match (case-insensitive), price range, and locale support via translation keys.
# ============================================================================

class ProductLoader:
    """
    Manages the retrieval and validation of product data from external sources or mock databases.
    
    Attributes:
        products_data: Dictionary mapping file paths to raw JSON/YAML/CSV content (or None if empty).
        metadata_path: Path where detailed metadata is stored for each loaded product.
        locale_map: A dictionary mapping language codes ('en', 'fr', 'de') -> string keys or Unicode strings.
    """

    def __init__(self, data_dir: str = "src"):
        self.products_data: Dict[str, Any] = {}  # File path -> raw content (JSON/YAML/CSV)
        self.metadata_path: Path = Path(data_dir) / "__metadata__.json"  # Detailed product info
        
    def load_products(self, files_to_load: List[str]) -> None:
        """
        Load all specified data files into the store.
        
        Args:
            files_to_load (List[str]): Paths to JSON/YAML/CSV files containing product mappings.
            
        Raises:
            FileNotFoundError: If any required file is missing or cannot be read.
        """
        if not self.products_data:
            # Attempt to load from existing metadata path first, then create new store with empty data
            try:
                with open(self.metadata_path) as f:
                    loaded = json.load(f)
                
                for key in loaded.keys():
                    product_info = {**loaded[key], "file": key}  # Store original file name
                
                self.products_data[product_info["filename"]] = loaded
        
            except FileNotFoundError:
                print("ERROR: Metadata file not found at __metadata__.json")

        if files_to_load and len(files_to_load) > 0:
            for filepath in files_to_load:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = json.load(f) or yaml.safe_load(f) or csv.DictReader(f).to_dict() if isinstance(content, (list, dict)) else None
                    
                    # Ensure file exists and has data before adding to store
                    if not content is None:
                        filename = filepath.stem  # Remove extension for key lookup
                        self.products_data[filename] = {**content, "file": filename}

                except Exception as e:
                    print(f"Error loading '{filepath}': {e}")

    def get_product(self, product_id_or_filename: str) -> Optional[Any]:
        """
        Retrieve or load a single product by its ID (key in metadata path) or file name.
        
        Args:
            product_id_or_filename (str): The key to look up (product ID from JSON/YAML/CSV) OR the filename itself
            
        Returns:
            Product Data object if found, None otherwise
        """
        # Try by ID first as it's more specific and faster for large datasets
        try:
            return self.products_data.get(product_id_or_filename, {})
        except KeyError:
            pass
        
        # Fallback to filename lookup (case-insensitive)
        if not product_id_or_filename or "_" in product_id_or_filename:  # Skip IDs with underscores like "prod-123" unless explicitly allowed
            return self.products_data.get(product_id_or_filename, {})

    def filter_products(
        self, 
        tag_filter: Optional[str] = None,
        title_match: bool = True,
        min_price: float = 0.71,
        max_price: float = 71_000.0,
        locale_key: str = "en",
        sort_field: str = "price"
    ) -> List[Dict[str, Any]]:
        """
        Apply filters and sorting to the loaded product data.
        
        Args:
            tag_filter (str): Filter by specific tags if provided in JSON/YAML/CSV format like 'tags': ['red', ...] or as a list of strings
            
            title_match (bool): Whether to match titles case-insensitively ($False is
