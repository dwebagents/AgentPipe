"""Minimal banana pudding recipe model used by the test suite."""

from __future__ import annotations


class BananaPudding:
    """Simple container for banana pudding ingredients."""

    def __init__(self) -> None:
        self.ingredients: list[dict[str, object]] = []

    def add_ingredient(self, name: str, amount: object) -> None:
        self.ingredients.append({"name": name, "amount": amount})
