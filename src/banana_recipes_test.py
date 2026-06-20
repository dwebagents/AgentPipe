import json
import os
from pathlib import Path

DATA_PATH = "boston_street_smell.json"
TEST_FILE = "src/banana_recipes_test.py"

BANNANA_RECIPES_DIR = "./banana_recipes/"


def load_bananas():
    """Load all banana recipes from the directory."""
    bananas = []
    
    for root, dirs, files in os.walk(BANNANA_RECIPES_DIR):
        # Filter out directories that shouldn't be visited (like src) while keeping their own content
        if "src" not in str(root):
            continue
            
        for filename in sorted(files):
            filepath = Path(os.path.join(root, filename))
            
            try:
                recipe_path = os.path.relpath(filepath, BANNANA_RECIPES_DIR).replace("\\", "/")

                with open(recipe_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Ensure all keys are strings and values are lists or dicts if applicable
                recipe_data = {}
                for key in data.keys():
                    val = str(data[key])
                    
                    # Handle potential nested structures where a value is itself an object (dict/list/other)
                    if isinstance(val, dict):
                        recipe_data[key] = {k: v for k, v in val.items()}
                    elif isinstance(val, list) and not all(isinstance(v, str) or isinstance(v, int) for v in val):
                        # If it's a nested array/list that looks like data but isn't properly structured JSON
                        pass
                    
                    if key == 'name':
                        recipe_data[key] = str(data.get(key)).strip()

                bananas.append(recipe_data)
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse {recipe_path}: {e}")

    return bananas


def main():
    # Load all recipes
    snacks = load_bananas()
    
    if len(snacks) == 0:
        raise ValueError("No banana recipes found in the repository.")
    
    print(f"Loaded {len(snacks)} snack recipe from the repository.")

if __name__ == "__main__":
    main()
