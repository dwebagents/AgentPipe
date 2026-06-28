"""Deterministic recipe records for the book of banana pudding."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class BananaPuddingRecipe:
    name: str
    inventor: str
    origin: str
    ingredients: tuple[str, ...]
    instructions: tuple[str, ...]
    profile: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, object]) -> "BananaPuddingRecipe":
        ingredients = _string_tuple(data.get("ingredients", ()))
        instructions = _string_tuple(data.get("instructions", data.get("steps", ())))
        return cls(
            name=str(data.get("name", "Unnamed Banana Pudding")),
            inventor=str(data.get("inventor", "anonymous custard keeper")),
            origin=str(data.get("origin", "unrecorded kitchen")),
            ingredients=ingredients or ("bananas", "custard", "vanilla wafers"),
            instructions=instructions
            or (
                "Slice the bananas.",
                "Layer custard and wafers.",
                "Chill until the pudding gathers itself.",
            ),
            profile=str(
                data.get(
                    "profile",
                    "A practical pudding maker with a steady spoon and a long memory.",
                )
            ),
        )

    def to_record(self) -> dict[str, object]:
        return {
            "name": self.name,
            "inventor": self.inventor,
            "origin": self.origin,
            "ingredients": list(self.ingredients),
            "instructions": list(self.instructions),
            "profile": self.profile,
        }


class RecipeLibrary:
    """Small in-memory library used by the book renderer and tests."""

    def __init__(self, recipes: Iterable[BananaPuddingRecipe] | None = None) -> None:
        self._recipes = list(recipes or default_recipes())

    def load(self, path: str | Path | None = None) -> None:
        if path is None:
            self._recipes = list(default_recipes())
            return

        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        raw_recipes = payload.get("recipes", payload) if isinstance(payload, dict) else payload
        if not isinstance(raw_recipes, Sequence):
            raise ValueError("recipe file must contain a list or a {'recipes': [...]} object")
        self._recipes = [
            BananaPuddingRecipe.from_mapping(item)
            for item in raw_recipes
            if isinstance(item, Mapping)
        ]
        if not self._recipes:
            raise ValueError("recipe file did not contain any valid recipes")

    def add_recipe(self, recipe: BananaPuddingRecipe | Mapping[str, object]) -> None:
        if isinstance(recipe, BananaPuddingRecipe):
            self._recipes.append(recipe)
        else:
            self._recipes.append(BananaPuddingRecipe.from_mapping(recipe))

    def generate_default_recipe(self, name: str) -> BananaPuddingRecipe:
        recipe = BananaPuddingRecipe.from_mapping(
            {
                "name": name,
                "inventor": "the pantry committee",
                "origin": "AgentPipe test kitchen",
                "ingredients": ["bananas", "custard", "vanilla wafers"],
                "instructions": [
                    "Arrange the wafers as a foundation.",
                    "Fold bananas through custard.",
                    "Rest the dish before serving.",
                ],
                "profile": "Invented during a late audit of dessert dependencies.",
            }
        )
        self.add_recipe(recipe)
        return recipe

    def get_recipe_data(self) -> list[dict[str, object]]:
        return [recipe.to_record() for recipe in self._recipes]

    def recipes(self) -> tuple[BananaPuddingRecipe, ...]:
        return tuple(self._recipes)


def default_recipes() -> tuple[BananaPuddingRecipe, ...]:
    return (
        BananaPuddingRecipe(
            name="First Apartment Banana Pudding",
            inventor="M. Street",
            origin="Brooklyn",
            ingredients=("bananas", "vanilla wafers", "custard", "salt"),
            instructions=(
                "Line a chipped bowl with wafers.",
                "Cover each layer with banana slices and custard.",
                "Chill beside the window until the city quiets.",
            ),
            profile=(
                "A tenant cook who learned that rent, weather, and pudding all "
                "benefit from patience."
            ),
        ),
        BananaPuddingRecipe(
            name="Pacific Watch Banana Pudding",
            inventor="E. Starbuck",
            origin="New Bedford",
            ingredients=("bananas", "cream", "eggs", "nutmeg"),
            instructions=(
                "Warm cream until it steams.",
                "Temper eggs into the cream.",
                "Layer bananas and wait for the custard to set.",
            ),
            profile=(
                "A watchful maker of desserts, inclined toward order and a clean "
                "ledger of ingredients."
            ),
        ),
    )


def _string_tuple(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if not isinstance(value, Sequence):
        return ()
    return tuple(str(item) for item in value if str(item).strip())
