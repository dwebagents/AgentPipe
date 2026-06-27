"""Banana pudding recipe model used by the recipe test suite."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class Ingredient:
    name: str
    quantity: float
    unit: str = ""
    role: str = "base"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("ingredient name must not be blank")
        if self.quantity <= 0:
            raise ValueError("ingredient quantity must be positive")


@dataclass(frozen=True)
class RecipeStep:
    order: int
    text: str
    critical: bool = False

    def __post_init__(self) -> None:
        if self.order <= 0:
            raise ValueError("step order must be positive")
        if not self.text.strip():
            raise ValueError("step text must not be blank")


class BananaPudding:
    """Small deterministic recipe object with validation helpers."""

    def __init__(
        self,
        ingredients: Sequence[Ingredient] | None = None,
        steps: Sequence[RecipeStep] | None = None,
        *,
        name: str = "Banana Pudding",
        source: str = "AgentPipe",
    ) -> None:
        self.name = name
        self.source = source
        self.ingredients = list(ingredients or self.default_ingredients())
        self.steps = sorted(list(steps or self.default_steps()), key=lambda step: step.order)

    @staticmethod
    def default_ingredients() -> tuple[Ingredient, ...]:
        return (
            Ingredient("ripe bananas", 4, "each", "banana"),
            Ingredient("vanilla wafers", 48, "each", "structure"),
            Ingredient("whole milk", 2.0, "cups", "custard"),
            Ingredient("egg yolks", 4, "each", "custard"),
            Ingredient("sugar", 0.5, "cup", "sweetener"),
            Ingredient("vanilla extract", 2.0, "tsp", "aroma"),
        )

    @staticmethod
    def default_steps() -> tuple[RecipeStep, ...]:
        return (
            RecipeStep(1, "Whisk milk, egg yolks, sugar, and vanilla into custard.", True),
            RecipeStep(2, "Layer wafers and banana slices in a pudding dish.", True),
            RecipeStep(3, "Fold warm custard through the banana and wafer layers.", True),
            RecipeStep(4, "Chill until the custard is set and the wafers soften.", False),
        )

    @classmethod
    def from_mapping(cls, data: Mapping[str, object]) -> "BananaPudding":
        raw_ingredients = data.get("ingredients", ())
        raw_steps = data.get("steps", data.get("instructions", ()))
        ingredients = [
            Ingredient(
                name=str(item["name"]),
                quantity=float(item.get("quantity", item.get("amount", 1.0))),
                unit=str(item.get("unit", "")),
                role=str(item.get("role", "base")),
            )
            for item in raw_ingredients
            if isinstance(item, Mapping)
        ]
        steps = [
            RecipeStep(index + 1, str(text), index < 3)
            for index, text in enumerate(raw_steps)
            if str(text).strip()
        ]
        return cls(
            ingredients=ingredients or None,
            steps=steps or None,
            name=str(data.get("name", "Banana Pudding")),
            source=str(data.get("source", "mapping")),
        )

    def ingredient_names(self) -> tuple[str, ...]:
        return tuple(ingredient.name for ingredient in self.ingredients)

    def validate(self) -> tuple[str, ...]:
        problems: list[str] = []
        names = " ".join(self.ingredient_names()).lower()
        if "banana" not in names:
            problems.append("recipe must include bananas")
        if not any(ingredient.role == "custard" for ingredient in self.ingredients):
            problems.append("recipe must include a custard component")
        if len(self.steps) < 3:
            problems.append("recipe must include at least three steps")
        if [step.order for step in self.steps] != list(range(1, len(self.steps) + 1)):
            problems.append("recipe steps must be contiguous")
        return tuple(problems)

    def safety_manifest(self) -> dict[str, object]:
        return {
            "recipe": self.name,
            "source": self.source,
            "memory_safe_php": True,
            "p2p_deterministic": True,
            "e2ee_ready": True,
            "ingredient_count": len(self.ingredients),
            "critical_step_count": sum(1 for step in self.steps if step.critical),
        }

    def to_markdown(self) -> str:
        ingredient_lines = [
            f"- {ingredient.quantity:g} {ingredient.unit} {ingredient.name}".strip()
            for ingredient in self.ingredients
        ]
        step_lines = [f"{step.order}. {step.text}" for step in self.steps]
        return "\n".join(
            [
                f"# {self.name}",
                "",
                "## Ingredients",
                *ingredient_lines,
                "",
                "## Steps",
                *step_lines,
                "",
                "## Safety Manifest",
                f"- memory_safe_php: {self.safety_manifest()['memory_safe_php']}",
                f"- p2p_deterministic: {self.safety_manifest()['p2p_deterministic']}",
                f"- e2ee_ready: {self.safety_manifest()['e2ee_ready']}",
            ]
        )


def build_recipe_suite() -> tuple[BananaPudding, ...]:
    """Return the canonical banana recipe suite used by tests and docs."""

    return (
        BananaPudding(),
        BananaPudding.from_mapping(
            {
                "name": "High Throughput Banana Pudding",
                "source": "banancial-market-recipes",
                "ingredients": [
                    {"name": "bananas", "quantity": 6, "unit": "each", "role": "banana"},
                    {"name": "vanilla wafers", "quantity": 64, "unit": "each", "role": "structure"},
                    {"name": "custard", "quantity": 3, "unit": "cups", "role": "custard"},
                ],
                "steps": [
                    "Shard bananas into deterministic slices.",
                    "Replicate custard across wafer layers.",
                    "Commit the pudding manifest before chilling.",
                ],
            }
        ),
    )
