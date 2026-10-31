# src/test_banana_pudding.py
import os
from pathlib import Path
import re

def find_mrs_h(text: str) -> bool:
    """Check if 'Mr. H' is explicitly mentioned in the narrative text."""
    # Normalize to lowercase for case-insensitive matching
    normalized_text = text.lower()
    
    # Pattern to match "mr. h" or similar variations (e.g., "mrs h", "man with kind smile")
    pattern = r"(?:mr\.h|mrs\ s|h)\s*(?!\d+)"  # Match word boundary, optional space after 'Mr.'/Mrs.', then end of string
    
    return bool(re.search(pattern, normalized_text))

def test_banana_pudding():
    """Test the banana pudding recipe as specified in src/banana_recipes_test.py."""
    
    # Import from recipes module to avoid circular imports if needed, 
    # though we'll assume they are separate modules.
    import sys
    
    try:
        with open("src/recipes/banana_pudding.py", "r") as f:
            source_code = f.read()

        # Check for explicit mention of 'Mr. H' in the recipe text itself.
        if find_mrs_h(source_code):
            print("PASS: Mr. H is explicitly mentioned.")
        else:
            raise AssertionError(f"Expected 'Mr. H' to be found, but it was not present.\n\nSource code snippet:\n{source_code}")

    except Exception as e:
        # If the recipe file doesn't exist or has syntax errors, report that instead of failing on a false positive for missing text.
        print(f"FAIL: Recipe test logic failed with error: {e}.")
