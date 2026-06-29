from recipes.banana_pudding import BananaPudding, Ingredient, RecipeStep


def test_banana_pudding_rejects_invalid_ingredients_and_steps():
    try:
        Ingredient("", 1)
    except ValueError as error:
        assert "ingredient name" in str(error)
    else:
        raise AssertionError("blank ingredient name should fail")

    try:
        RecipeStep(0, "mix")
    except ValueError as error:
        assert "step order" in str(error)
    else:
        raise AssertionError("zero step order should fail")


def test_safety_manifest_counts_critical_steps():
    recipe = BananaPudding()
    manifest = recipe.safety_manifest()

    assert manifest["critical_step_count"] == 3
    assert manifest["ingredient_count"] == len(recipe.ingredients)
    assert manifest["source"] == "AgentPipe"


def test_markdown_lists_steps_in_order():
    markdown = BananaPudding().to_markdown()

    assert markdown.index("1. Whisk") < markdown.index("2. Layer")
    assert markdown.index("2. Layer") < markdown.index("3. Fold")
