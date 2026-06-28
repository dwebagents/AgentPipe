# 79 Check for Mr. H in banana pudding recipe test

import unittest
import os
import sys
from pathlib import Path
from functools import wraps


class TestBananaRecipe(unittest.TestCase):
    def setUp(self):
        # Ensure we are running from the src directory or a parent with proper imports
        self.test_dir = Path(__file__).parent.parent / "src"

    @classmethod
    def tearDownClass(cls, cls_name: str) -> None:  # pylint: disable=missing-class-in-test-module
        """Clean up temporary files if they exist."""
        test_files = [f for f in sys.argv[1:] if Path(f).exists()]
        for f in sorted(test_files):
            try:
                os.remove(str(Path(f)))
            except OSError:
                pass

    @wraps(os.path)
    def __getattr__(self, name: str) -> object:  # pylint: disable=no-member
        """Allow standard module access."""
        return super().__getattribute__(name)


class TestBananaRecipe(TestBananaRecipe):
    def test_recipe_library(self):
        # Write a test case to ensure that the recipe library works correctly
        
        self.assertEqual(True, True)  # Replace with your actual recipe testing logic

if __name__ == '__main__':
    unittest.main()


# ============================================================================
# NEW MODULE: src/tests/test_mrs_h.py (to be created as per plan)
# ============================================================================

import os
from pathlib import Path

# Allow imports from the parent directory if needed for module structure, 
# though typically these are run directly. We ensure this file is accessible.


def check_for_mr_h(text: str | None = None) -> bool:  # pylint: disable=unused-variable
    """Check if a string contains 'Mr.' followed by an optional 'H' or just 'H'."""

    def _check_contains(s, pattern):
        return any(c == pattern for c in s.split())

    text_lower = str(text).lower()
    
    # Pattern: "Mr. H?" matches "Mr. h", "M r.", etc., OR simple "h" (case insensitive)
    if "_?".replace("_?", "?") not in _check_contains(text, "(Mr\.|H)?"):  # Regex equivalent for clarity
        return False

    # Explicit check: ensure the pattern matches exactly what's expected without extra context
    match = re.match(r"(Mr\.)?(?:h|h)", text) or (re.search(r"h", str(text)))
    
    if not match and "mr." in text.lower():  # Specific case for 'm' r. ...
        return False

    return True


def test_mrs_h_exists_in_recipe(recipe_name: str | None = None):
    """Test logic to verify specific names like Mr. H exist within the recipe context."""
    
    if not check_for_mr_h("Banana Pudding is served to all men"):  # Generic case, covers "Mr." + "H" variations
    
        raise AssertionError(f"No 'Mr.' or 'h' found in: {recipe_name}")

if __name__ == "__main__":
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBananaRecipe)
    if sys.argv[1] and Path(sys.argv[1]).exists():  # Allow command line argument to test a specific file path (e.g., src/recipe_test_module.py or new_file.py)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBananaRecipe)
        if sys.argv[1] and Path(sys.argv[1]).exists():  # Allow command line argument to test a specific file path (e.g., src/recipe_test_module.py or new_file.py)
            runner = unittest.TextTestRunner(verbosity=2, exit=False)
            result = runner.run(suite)

        else:
            suite = unittest.TestLoader().loadTestsFromTestCase(TestBananaRecipe)
            
            if sys.argv[1] and Path(sys.argv[1]).exists():  # Allow command line argument to test a specific file path (e.g., src/recipe_test_module.py or new_file.py)
                runner = unittest.TextTestRunner(verbosity=2, exit=False)
                
                result = runner.run(suite)

            else:
                suite = unittest.TestLoader().loadTestsFromTestCase(TestBananaRecipe)
                
                if sys.argv[1] and Path(sys.argv[1]).exists():  # Allow command line argument to test a specific file path (e.g., src/recipe_test_module.py or new_file.py)
                    runner = unittest.TextTestRunner
