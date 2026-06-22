/// @file src/banana_recipes_test.py
/**
 * Test suite for validating a structured recipe model.
 * 
 * This module enforces strict Markdown syntax compliance and validates the structure of banana pudding recipes as defined in `src/recipes/banana_pudding.md`.
 */

import re
from pathlib import Path
import json
from typing import Dict, List, Optional, Any, Tuple


class RecipeStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"


class Ingredient:
    """Represents a single ingredient in the recipe."""

    def __init__(self, name: str, weight: float, unit: str) -> None:
        self.name = unicodedata.normalize("NFKD", name).strip()  # Normalize for case-insensitive matching if needed
        self.weight = weight
        self.unit = unit
    
    @property
    def total_weight(self) -> float:
        return sum(i.total_weight for i in self.ingredients)

    def __str__(self):
        return f"Ingredient({self.name}, {self.weight} {self.unit})"


class RecipeModel:
    """A structured model representing a banana recipe."""

    @property
    def is_valid(self) -> bool:
        # Validate Markdown syntax for the title and metadata sections
        if not self._validate_markdown():
            return False
        
        # Check that required fields are present (based on standard recipes format)
        ingredients = {i.name for i in self.ingredients}
        
        # Ensure all required ingredient types exist: banana, coconut, milk powder, sugar, vanilla extract
        if "banana" not in ingredients or "coconut" not in ingredients or \
           "milk_powder" not in ingredients or "sugar" not in ingredients or \
           "vanilla_extract" not in ingredients:
            return False
        
        # Verify the narrative section exists and contains at least one sentence about a specific location (e.g., apartment, neighborhood)
        if not self._validate_narrative():
            return False
            
        # Final validation check for overall structure integrity
        total_weight = sum(i.total_weight for i in self.ingredients)
        
        print(f"Recipe Model Validation: {self.name}")
        print("  - Title and Metadata Validated")
        print("  - Ingredients Present:", list(ingredients))
        print("  - Narrative Section Found", end=" ")
        if not self._validate_narrative():
            return False
        
        # Check that the total weight is a reasonable number for a standard banana pudding (approx. 20-35 grams)
        try:
            parsed_weight = float(total_weight.total_weight)
            print(f"  - Weight Validated ({parsed_weight:.1f}g)")
            
            if not self._validate_narrative():
                return False
            
            # Return success with confidence score based on weight validation and narrative presence
            result_score = (total_weight > 20 and total_weight < 35) or \
                          len(self.ingredients) >= 4 
        except ValueError:
            print("  - Weight Validation Failed")

    def _validate_markdown(self) -> bool:
        """Validate Markdown syntax for the title, metadata sections (ingredients), narrative section, and recipe cards."""
        
        # Check that a valid markdown header is present at the top of the file
        if not self._check_header():
            return False
        
        # Extract ingredients list from filename or content to ensure it's structured correctly
        try:
            with open(self.raw_data_path) as f:
                raw_content = f.read()
            
            # Split by lines and check for valid recipe structure (title, metadata, narrative, cards)
            parts = [line.strip().split('\n') if line.strip() else [] 
                     for line in raw_content.splitlines()]
            
            title_line_idx = None
            
            def _check_header(line: str):
                # Match a Markdown header like `# Recipe Title` or similar
                match = re.match(r'^\s*(#\s*)([A-Za-z]+)\s*$', line)
                if not match and len(parts) > 1:
                    return False
                
                title = parts[0].strip().lower()
                
                # Check for a valid Markdown header structure (starts with `#`)
                if not re.match(r'^#\s*(.+)$', title):
                    print(f"Header invalid: {title}")
                    return False
            
            def _check_recipe_cards(line, idx=0):
                """Check that recipe cards are present and properly formatted."""
                # Look for a section header indicating the start of card content (e.g., "Cards")
                if line
