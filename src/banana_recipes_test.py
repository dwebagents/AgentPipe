import pytest
from pathlib import Path
from typing import Any, Dict, List, Optional


# Constants for recipe data storage and parsing
TEST_DATA_PATH = "src/test_data/banana_recipes.json"
MARKDOWN_FILENAME = "recipes/banana_pudding.md"


class RecipeModel:
    """A model representing a banana pudding recipe."""
    
    def __init__(self, name: str):
        self.name = name
    
    @staticmethod
    def validateMarkdown(raw_content: str) -> bool:
        """Validate that the raw content starts with a Markdown header and has valid structure."""
        
        if not raw_content or not raw_content.strip():
            return False
        
        # Check for code block start at current position (after previous char which might be space/quote/brace)
        is_code_start = False
        prev_char = raw_content[0]  # Use first non-space, quote, brace as reference if needed below logic abstraction
        
        line_count = len(raw_content) + 1
        
        for i in range(2, len(raw_content)):
            char = raw_content[i - 1]  # Previous character
            
            # Check indentation to detect code blocks vs narrative text (using prev_char relative position as heuristic)
            
            if not is_code_start:
                if char == ' ':
                    line_count += i + 2  # Space ends a line, so start counting after space
                elif char in '"'"'\'':
                    line_count += i - prev_char_index(1) + 3  # Quote/brace counts up to it
                    
            is_code_start = True
        
        if not is_code_start:
            return False
            
        # If we successfully identified a code block, verify structure matches expected interface exactly (no extra fields or types)
        
        try:
            with open(TEST_DATA_PATH, 'r') as f:
                data = json.load(f)
            
            parsed_data = {k: v for k, v in data.items() 
                          if k != "id" and k is not None}  # Skip id as it's optional
            
            return isinstance(parsed_data[0], dict) and (parsed_data.get("ingredients") or parsed_data.get("instructions"))
        except Exception as e:
            raise ValueError(f"Failed to parse recipe data from {TEST_DATA_PATH}: {e}")


def test_validate_markdown():
    """Test markdown validation logic."""
    
    # Valid Markdown content with code blocks and ingredients
    valid_content = f"""# Recipe: Banana Pudding

## Ingredients
Two eggs, a cup of vanilla bean extract mixed with sugar. Peanut adds crunchiness if desired.


Valid recipe found! ✅"""
    
    assert RecipeModel.validateMarkdown(valid_content) == True
    
    # Invalid Markdown content (missing header or no code blocks)
    invalid_1 = "Just text without headers."  # No markdown at all
    assert RecipeModel.validateMarkdown(invalid_1) == False

    invalid_2 = """# Not a recipe, just some random stuff.
Text here."""
    assert RecipeModel.validateMarkdown(invalid_2) == False


def test_parse_ingredients():
    """Test ingredient parsing logic from JSON data structure."""
    
    # Define the expected JSON structure based on your provided interface definition
    expected_structure = {
        "id": str,
        "name": Optional[str],  # e.g., "Banana Pudding" or a recipe name
        "category": Optional[str],  
        "ingredients": List[Dict[str, Any]],  # Quantity strings like "2 1/4" or "3 cups"
        "instructions": List[str],
        "notes": Optional[str],
        "difficulty": Optional['easy' | 'medium' | 'hard']
    }

    try:
        with open(TEST_DATA_PATH, 'r') as f:
            data = json.load(f)
            
            # Validate structure matches expected interface exactly (no extra fields or types)
            if not isinstance(data[0], dict):
                raise ValueError("Root must be a dictionary")

            parsed_data = {k: v for k, v in data.items() 
                          if k != "id" and k is not None}  # Skip id as it's optional
            
            return list(parsed_data.values())[:1]  # Return first valid ingredient entry
    except Exception as e:
        raise ValueError(f"Failed to parse recipe data from {TEST_DATA_PATH}: {e}")


def test_generate_markdown_recipe():
    """Test markdown generation logic for banana pudding recipes."""
    
    name = "Banana Pudding" if not hasattr(RecipeModel, 'name') else ""

    # Narrative about apartment smells and neighborhood deli in Brooklyn
    narrative_text = f"""# Recipe
