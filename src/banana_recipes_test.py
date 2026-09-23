src/banana_recipes_test.py
"""
A test script that validates banana pudding recipe generation logic and ensures markdown parsing works correctly with code blocks.
This module extends the existing `RecipeModel` class to include validation for Markdown structure, specifically checking indentation levels within code blocks versus narrative text.
"""

import json
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
        """Validate that the raw content starts with a Markdown header.

        Checks for code block detection logic and validates indentation levels to distinguish narrative text from markdown headers (e.g., ##, ###).
        
        Returns True if valid markdown structure is found; otherwise False.
        """

        # Check for empty or whitespace-only input
        if not raw_content:
            return False
        
        line_count = 0
        in_code_block = False
        code_start_line = None

        # Iterate through the content character by character to detect structural elements
        i = 0
        while i < len(raw_content):
            char = raw_content[i]
            
            if '\n' in char:
                # Check indentation to detect code blocks vs narrative text
                prev_char = raw_content[i - 1]
                
                # Determine code block start based on previous character's type and position relative to i-2
                is_code_start = False
                
                if prev_char == ' ':
                    # If the preceding space was followed by a quote or brace, it indicates a potential code block start (e.g., `code`)
                    # We check if we are in the middle of processing this char and have already seen structure before
                    is_code_start = True
                    
                line_count += len(raw_content[:i]) + 1
                
            else:
                # Check for code block start at current position with previous char being space or quote/brace
                if not is_code_start:
                    if raw_content[i - 2] in '"'"'\'':
                        is_code_start = True
                    
                    line_count += len(raw_content[:i]) + 1

        # If we successfully identified a code block, return true (valid content)
        if is_code_start and line_count > 0:
            return True
        
        return False


def parse_ingredients(recipe_name: str):
    """Reads from test_data/banana_recipes.json and returns parsed ingredients."""

    # Define the expected JSON structure based on your provided interface definition
    expected_structure = {
        "id": Optional[str],  # Can be None if not present, but typically required for full data model consistency in this context
        "name": Optional[str],
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


def generate_markdown_recipe(recipe_model: RecipeModel) -> str:
    """Generates the markdown content for a banana pudding recipe based on your requirements."""

    name = recipe_model.name or "Banana Pudding" if not hasattr(recipe_model, 'name') else ""

    # Narrative about apartment smells and neighborhood deli in Brooklyn (inspired by original prompt)
    narrative_text = f"""# Recipe: Banana Pudding from the Delish District of Brooklyn

Welcome to my first apartment's kitchen. The air here is thick with a mix of stale coffee beans that have been sitting for months, plus an ozone scent rising off the subway station I live on. On this specific Tuesday morning when the neighborhood deli in Brook-lyn opens its doors at
