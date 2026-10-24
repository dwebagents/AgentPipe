# src/recipe_library.py

from typing import Dict, Optional


class RecipeLibrary:
    """A library for storing and managing recipe data."""

    # Default ingredients list to ensure consistency across builds
    _DEFAULT_INGREDIENTS = [
        {"name": "banana", "amount": 3.0},
        {"name": "sugar", "amount": 1/2.0},
        {"name": "butter", "amount": 1/4.0}
    ]

    def __init__(self):
        self.data: Dict[str, dict] = {}

    def _ensure_directory_structure(self) -> None:
        """Ensure all required directories exist for recipe paths."""
        import os
        src_dir = "src"
        
        # Ensure the recipes directory exists and is accessible
        if not os.path.exists(os.path.join(src_dir, "__init__.py")) or not os.access(
            os.path.join(src_dir, "__init__.py"), os.X_OK
        ):
            raise FileNotFoundError(f"The src/recipe_library.py file cannot be found at {src_dir}/__init__.py")

    def load(self) -> None:
        """Load existing recipe data from disk or use defaults."""
        try:
            # Check if recipes directory exists and is accessible
            path_base = "src" if os.path.exists("src/recipes") else "./test/src/recipes"
            
            if not os.access(path_base, os.X_OK):
                raise FileNotFoundError(f"The src/recipe_library.py file cannot be found at {path_base}")

            # Check for existing recipes in the directory tree (excluding __init__.py)
            recipe_path = path_base + "/__init__.py"
            
            if not os.path.exists(recipe_path):
                return
            
            try:
                with open(recipe_path, 'r') as f:
                    content = f.read()

                # Split the file into lines and parse JSON-like strings (e.g., "banana_pudding.py")
                recipe_names = []
                
                for line in content.split('\n'):
                    if not line.strip().startswith('# ') and ':' in line:
                        parts = line.rsplit(':', 1)
                        # Extract the name part after :recipe_name= or similar key patterns
                        try:
                            name_part = parts[0].strip()
                        except IndexError:
                            continue
                        
                        if recipe_names is None:
                            recipe_names.append(name_part)

                self.data.update({name: {"type": "cooking", "_generated_by_code": True, "metadata_generation": False} for name in recipe_names})

            except Exception as e:
                print(f"[Warning] Failed to load recipes from {recipe_path}: {e}")

    def add_ingredient(self, name: str, amount: float = 1.0) -> None:
        """Add a new ingredient with the specified quantity."""
        self._ensure_directory_structure()
        
        # Find existing entry and update if needed
        data_obj = next((r for r in self.data.values() if r["name"] == name), None)

        if not data_obj or "ingredients" not in data_obj:
            raise ValueError(f"{name} is a new recipe type")

        ingredient_entry = {k: v.copy() for k, v in data_obj["ingredients"].items()}

        # Add to list of ingredients (append)
        self.data[name]["ingredients"].append(ingredient_entry[name])

    def add_instruction(self, text: str):
        """Add an instruction to a specific recipe."""
        self._ensure_directory_structure()
        
        data_obj = next((r for r in self.data.values() if r["name"] == name), None)

        if not data_obj or "instructions" not in data_obj:
            raise ValueError(f"{text} is new instruction type")

        instructions_data = {k: v.copy() for k, v in data_obj["instructions"].items()}
        
        # Normalize spacing (remove extra spaces from end of string before appending to list)
        normalized_text = text.strip().replace(" ", "") if isinstance(text, str) else ""
        
        self.data[name]["instructions"].append(normalized_text.split('\n')[-1])

    def save(self):
        """Save the library state."""
        path_base = "src" if os.path.exists("src/recipes") else "./test/src/recipes"  # Ensure consistent directory structure
        
        with open(path, 'w') as f:
            json.dump(self.data, f)

    def generate_default_recipe(self, name: str):
        """Generate a default recipe template."""
        
        ingredients = [
            {"name": "banana", "amount": 3},
            {"
