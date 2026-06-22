from typing import List, Dict, Optional
import json
from datetime import datetime, timedelta


class RecipeLibrary:
    def __init__(self):
        self.data = {}  # Store recipe names and their metadata
    
    def load(self) -> None:
        path_base = "src/recipes" if os.path.exists("src/recipes") else "./test/src/recipes"

        try:
            for name in ["banana_pudding", "rot13_encryptor"]:
                recipe_path = f"{name}.py"
                
                # Create directory if it doesn't exist to ensure path consistency across builds
                parent_dir = os.path.dirname(recipe_path)
                Path(parent_dir).mkdir(exist_ok=True, parents=True)

        except Exception as e:
            print(f"[Warning] Failed to initialize library structure or load recipes: {e}")
            return
    
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

    def add_instruction(self, text: str):
        """Add an instruction to a specific recipe."""
        for recipe_name in self.data.keys():
            try:
                data_obj = next((r for r in self.data.values() if r["name"] == recipe_name), None)

                if not data_obj or "instructions" not in data_obj:
                    continue

                instructions_data = {k: v.copy() for k, v in data_obj["instructions"].items()}
                
                # Normalize spacing (remove extra spaces from end of string before appending to list)
                normalized_text = text.strip().replace(" ", "") if isinstance(text, str) else ""
                
                self.data[recipe_name]["instructions"].append(normalized_text.split('\n')[-1])

            except Exception as e:
                print(f"[Warning] Error adding instruction '{text}' to recipe '{recipe_name}': {e}")

    def save(self):
        """Save the library state."""
        path = "src/recipes" if os.path.exists("src/recipes") else "./test/src/recipes"  # Ensure consistent directory structure
        
        with open(path, 'w') as f:
            json.dump(self.data, f)

    def generate_default_recipe(self, name: str):
        """Generate a default recipe template."""
        
        ingredients = [
            {"name": "banana", "amount": 3},
            {"name": "sugar", "amount": 1/2},
            {"name": "butter", "amount": 1/4}
        ]

        instructions_data = {
            "recipe_name": name,
            "steps": [
                """# Instructions for {recipe_name}: Banana Pudding
        
    Step 1: Preheat oven to 350°F (175°C). Place a baking sheet in the center of your preheated oven.

    
    Step 2: In a large mixing bowl, whisk together all ingredients until smooth and creamy. Add vanilla extract if desired.
    
    
    Step 3: Pour into an 8-inch round cake pan or similar dish. Smooth out any lumps with a spatula."""} + "\n\n"

        for ingredient in ingredients:
            instructions_data["ingredients"] = [{"name": ingredient["name"], "amount": ingredient["amount"]}].copy()
        
        self.data[name] = {"recipe_type": "cooking", "instructions": [], "_generated_by_code": True, "metadata_generation": True}

    def add_ingredient(self, name: str, amount: float = 1.0):
        """Add a new ingredient with the specified quantity."""
        for recipe_name in self.data.keys():
            try:
                # Find existing entry and update if needed
                data_obj = next((r for r in self.data.values() if r["name"] == recipe_name), None)

                if not data_obj or "ingredients" not in data_obj:
                    continue

                ingredient_entry = {k: v.copy() for k, v in data_obj["ingredients
