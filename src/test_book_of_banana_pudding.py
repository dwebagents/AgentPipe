import json

from book_of_banana_pudding import BookOfBananaPudding
from recipe_library import BananaPuddingRecipe, RecipeLibrary


def test_recipe_library_loads_default_recipe_records():
    library = RecipeLibrary()
    records = library.get_recipe_data()

    assert len(records) == 2
    assert records[0]["name"] == "First Apartment Banana Pudding"
    assert "bananas" in records[0]["ingredients"]


def test_recipe_library_loads_json_recipe_file(tmp_path):
    recipe_file = tmp_path / "recipes.json"
    recipe_file.write_text(
        json.dumps(
            {
                "recipes": [
                    {
                        "name": "Harbor Pudding",
                        "inventor": "Queequeg's Cook",
                        "origin": "Nantucket",
                        "ingredients": ["banana", "cream"],
                        "instructions": ["Slice.", "Stir.", "Chill."],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    library = RecipeLibrary()
    library.load(recipe_file)

    assert library.get_recipe_data()[0]["name"] == "Harbor Pudding"
    assert library.get_recipe_data()[0]["origin"] == "Nantucket"


def test_book_renders_melville_style_chapter():
    recipe = BananaPuddingRecipe.from_mapping(
        {
            "name": "Quarterdeck Pudding",
            "inventor": "Ahab's Steward",
            "origin": "the Pequod",
            "ingredients": ["banana", "custard"],
            "instructions": ["Watch the bowl.", "Serve at dawn."],
        }
    )
    book = BookOfBananaPudding(RecipeLibrary([recipe]))
    manuscript = book.render_manuscript()

    assert manuscript.startswith("# The Book of Banana Pudding")
    assert "Call me Pudding." in manuscript
    assert "Ahab's Steward" in manuscript
    assert "### Ingredients" in manuscript


def test_book_exports_markdown_and_minimal_pdf(tmp_path):
    book = BookOfBananaPudding()
    markdown_path = book.export_to_markdown(tmp_path / "book.md")
    pdf_path = book.export_to_pdf(tmp_path / "book.pdf")

    assert markdown_path.read_text(encoding="utf-8").startswith(
        "# The Book of Banana Pudding"
    )
    pdf_bytes = pdf_path.read_bytes()
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"Book of Banana Pudding" in pdf_bytes
    assert b"startxref" in pdf_bytes
