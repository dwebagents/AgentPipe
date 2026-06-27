import unittest

from recipes.banana_pudding import BananaPudding, Ingredient, RecipeStep, build_recipe_suite


class TestBananaPudding(unittest.TestCase):
    def setUp(self):
        self.banana_pudding = BananaPudding()

    def test_default_recipe_has_required_components(self):
        self.assertIn("ripe bananas", self.banana_pudding.ingredient_names())
        self.assertIn("vanilla wafers", self.banana_pudding.ingredient_names())
        self.assertEqual(self.banana_pudding.validate(), ())

    def test_validation_reports_missing_banana_and_sparse_steps(self):
        recipe = BananaPudding(
            ingredients=[Ingredient("custard", 1, "cup", "custard")],
            steps=[RecipeStep(1, "Start."), RecipeStep(3, "Skip a number.")],
        )

        self.assertIn("recipe must include bananas", recipe.validate())
        self.assertIn("recipe must include at least three steps", recipe.validate())
        self.assertIn("recipe steps must be contiguous", recipe.validate())

    def test_suite_contains_memory_safe_manifests(self):
        suite = build_recipe_suite()

        self.assertGreaterEqual(len(suite), 2)
        for recipe in suite:
            manifest = recipe.safety_manifest()
            self.assertTrue(manifest["memory_safe_php"])
            self.assertTrue(manifest["p2p_deterministic"])
            self.assertTrue(manifest["e2ee_ready"])


if __name__ == "__main__":
    unittest.main()
