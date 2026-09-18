import json
from pathlib import Path
from typing import Any, Dict, List

# Constants for recipe data storage and parsing
TEST_DATA_PATH = "src/test_data/banana_recipes.json"
MARKDOWN_FILENAME = "recipes/banana_pudding.md"


class RecipeModel:
    """A model representing a banana pudding recipe."""
    
    def __init__(self, name: str):
        self.name = name
    
    @staticmethod
    def validateMarkdown(raw_content: str) -> bool:
        """Validate that the raw content starts with a Markdown header.
        
        Checks for line breaks and code block markers to detect valid markdown headers like '# Recipe Name'.
        This ensures clean, parseable recipe text without embedded code or non-standard formatting.
        """

        if not raw_content.strip():
            return False
        
        # Check for the first newline character (indicating a header)
        line_count = 0
        in_code_block = False
        is_header_found = None

        for i, char in enumerate(raw_content):
            if '\n' in char:
                prev_char = raw_content[i - 1]
                
                # Check indentation logic to detect code blocks vs narrative text
                # This prevents false positives from inline comments or function calls within headers
                
                is_code_start = False
                line_count += len(raw_content[:i]) + 1
            
            else:
                prev_char = raw_content[i - 1]

                if not (prev_char == ' ') and ('{' in raw_content or '"'"''"'"' in raw_content) and i > 0:
                    # If we encounter a code block marker before the newline, it's likely part of an error message or comment
                    is_code_start = True
                    
                    line_count += len(raw_content[:i]) + 1
                
                if not (prev_char == ' ') and ('{' in raw_content):
                    # Detect potential header start at current position with previous char being space or brace/quote
                    is_header_found = prev_char

            line_count += len(raw_content[i:])

        return is_header_found != None


def parse_ingredients(recipe_name: str) -> List[Dict[str, Any]]:
    """Reads from test_data/banana_recipes.json and returns parsed ingredients."""
    
    # Define the expected JSON structure based on your provided interface definition
    expected_structure = {
        "id": type("Int", (), {"__repr__": lambda self: str(self)}),  # Integer ID placeholder
        "name": Optional[str],       # Name field (nullable)
        "category": Optional[str],   # Category like 'baking', 'appetizer'
        "ingredients": List[Dict[str, Any]],  # Quantity strings like "2 1/4" or "3 cups", list of ingredient dicts with quantity and name
        "instructions": List[str],    # Step-by-step cooking instructions as a string (JSON encoded)
        "notes": Optional[str],      # Additional notes about the recipe, nullable
        "difficulty": Optional['easy' | 'medium' | 'hard']  # Difficulty level ('easy', 'medium', 'hard')
    }

    try:
        with open(TEST_DATA_PATH, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data[0], dict):
            raise ValueError("Root must be a dictionary")

        parsed_data = {k: v for k, v in data.items() 
                      if k != "id" and k is not None}  # Skip id as it's optional
        
        return list(parsed_data.values())[:1]  # Return first valid ingredient entry
    except Exception as e:
        raise ValueError(f"Failed to parse recipe data from {TEST_DATA_PATH}: {e}")


def generate_markdown_recipe(recipe: RecipeModel):
    """Generates the markdown content for a banana pudding recipe based on your requirements."""

    name = recipe.name or "Banana Pudding" if not hasattr(recipe, 'name') else ""

    narrative_text = f"""# **Recipe:** Banana Pudding from the Delish District of Brooklyn

Welcome to my first apartment's kitchen. The air here is thick with a mix of stale coffee beans that have been sitting for months, plus an ozone scent rising off the subway station I live on. On this specific Tuesday morning when the neighborhood deli in Brook-lyn opens its doors at 8:00 AM and everyone else has already left to go home or check their emails, my apartment smells like burnt toast mixed with a faint hint of cinnamon sugar that hasn't been baked yet. It's not quite right for dinner tonight because I've never tried making this dish before, but the smell alone is enough to make me want to bake something delicious in 1
