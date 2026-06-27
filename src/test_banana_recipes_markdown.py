from recipes.banana_pudding import BananaPudding, build_recipe_suite


def validate_markdown_recipe(markdown: str) -> bool:
    required_sections = (
        "# ",
        "## Narrative",
        "## Ingredients",
        "## Steps",
        "## Safety Manifest",
    )
    return bool(markdown.strip()) and all(section in markdown for section in required_sections)


def test_markdown_recipe_output_has_required_sections():
    markdown = BananaPudding().to_markdown()

    assert validate_markdown_recipe(markdown)
    assert "ripe bananas" in markdown
    assert "memory_safe_php: True" in markdown


def test_markdown_recipe_uses_table_and_long_intro():
    markdown = BananaPudding().to_markdown()

    assert "| Ingredient | Quantity | Unit | Role |" in markdown
    assert "| ripe bananas | 4 | each | banana |" in markdown
    assert "first apartment" in markdown
    assert "neighborhood deli in Brooklyn" in markdown
    assert markdown.index("## Narrative") < markdown.index("## Ingredients")
    assert markdown.index("## Ingredients") < markdown.index("## Steps")


def test_data_driven_recipe_builds_from_mapping():
    recipe = BananaPudding.from_mapping(
        {
            "name": "Brooklyn Banana Pudding",
            "ingredients": [
                {"name": "bananas", "quantity": 3, "unit": "each", "role": "banana"},
                {"name": "custard", "quantity": 2, "unit": "cups", "role": "custard"},
                {"name": "vanilla wafers", "quantity": 32, "unit": "each", "role": "structure"},
            ],
            "instructions": [
                "Slice bananas.",
                "Layer custard.",
                "Chill before serving.",
            ],
        }
    )

    assert recipe.name == "Brooklyn Banana Pudding"
    assert recipe.validate() == ()
    assert recipe.safety_manifest()["ingredient_count"] == 3


def test_canonical_recipe_suite_is_deterministic():
    first = [recipe.to_markdown() for recipe in build_recipe_suite()]
    second = [recipe.to_markdown() for recipe in build_recipe_suite()]

    assert first == second
    assert len(first) == 2
