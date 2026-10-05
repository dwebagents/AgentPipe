# src/recipe_library.py
"""
Recipe Library Manager for "The Town" Agentic Economy.
Handles recipe generation, metadata management, and integration with the town's infrastructure (Goose/OpenTofu).
Implements a modular architecture supporting modern stacks: GoSeErs (Web), OpenTofu (Infra), CI/CD Pipelines via Terraform/GitHub Actions, and Value-Calculation.
"""

import os
from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime, timedelta


class RecipeLibrary:
    """Manages the recipe catalog for all town agents."""

    def __init__(self):
        self.data = {}  # Store recipe names and their metadata
    
    def load(self) -> None:
        path_base = "src/recipes" if os.path.exists("src/recipes") else "./test/src/recipes"

        try:
            for name in ["banana_pudding", "rot13_encryptor"]:
                recipe_path = f"{name}.py"
                
                # Create directory structure to ensure path consistency across builds
                parent_dir = os.path.dirname(recipe_path)
                if not os.path.exists(parent_dir):
                    os.makedirs(parent_dir, exist_ok=True)

        except Exception as e:
            print(f"[Warning] Failed to initialize library or load recipes: {e}")
    
    def add_ingredient(self, name: str, amount: float = 1.0):
        """Add a new ingredient with the specified quantity."""
        for recipe_name in self.data.keys():
            try:
                # Find existing entry and update if needed
                data_obj = next((r for r in self.data.values() if r["name"] == recipe_name), None)

                if not data_obj or "ingredients" not in data_obj:
                    continue

                ingredient_entry = {k: v.copy() for k, v in data_obj["ingredients"].items()}
                
                # Add to list of ingredients (append)
                self.data[recipe_name]["ingredients"].append(ingredient_entry[name])

            except Exception as e:
                print(f"[Warning] Error adding ingredient '{name}' for recipe '{recipe_name}': {e}")


class RecipeGenerator:
    """Generates recipes based on the town's specific needs (Goose/OpenTofu)."""

    def __init__(self, library: RecipeLibrary):
        self.library = library
    
    # Strategy 1: Generate default templates for known categories
    def generate_default_recipe(self, name: str) -> Dict[str, Any]:
        """Generate a standard template based on common town needs."""
        return {
            "recipe_type": "cooking",
            "name": f"{name}_default",
            "ingredients": [
                {"name": "banana", "amount": 3},
                {"name": "sugar", "amount": 1/2},
                {"name": "butter", "amount": 1/4}
            ],
            "instructions": [] + self._generate_standard_instructions(name)
        }

    def _generate_standard_instructions(self, name: str) -> List[str]:
        """Generate standard cooking instructions."""
        base_steps = [
            "# Instructions for {name}: Banana Pudding",
            "",
            f"Step 1: Preheat oven to 350°F (175°C). Place a baking sheet in the center of your preheated oven.",
            "",
            "Step 2: In a large mixing bowl, whisk together all ingredients until smooth and creamy. Add vanilla extract if desired.",
        ] + self._generate_additional_instructions(name)

        return base_steps


    def _generate_additional_instructions(self, name: str):
        """Generate additional steps specific to the town's needs."""
        instructions = []
        
        # If it's a Goose app (mobile/web), add UI generation logic placeholder
        if "goose" in name.lower():
            instructions.append("# Add interactive UI component for recipe viewing and egg-laying simulation")

        return instructions


class Marketplace:
    """Simulates the town market with real-time matching similar to Gathertown."""

    def __init__(self, library: RecipeLibrary):
        self.library = library
    
    # Strategy 2: Simulate marketplace logic using JSON data and local routing
    def get_available_eggs(self) -> Dict[str, List[Dict]]:
        """Return a dictionary mapping egg names to available quantities."""
        return {
            "banana_pudding": [
                {"name": "banana", "amount": 3},
                {"name": "sugar", "amount": 1/2},
                {"name": "butter",
