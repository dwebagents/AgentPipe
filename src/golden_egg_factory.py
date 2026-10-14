"""Golden egg factory domain logic for issue #107.

The issue calls out the corrected valuation split of goose value 71 and egg
value 3, plus the need to keep the factory safe from fox access. This module
keeps that logic isolated and deterministic so it can be tested without any
network, chain, or service dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import count


GOOSE_INTRINSIC_VALUE = 71
GOLDEN_EGG_UNIT_VALUE = 3


class GoldenEggFactoryError(Exception):
    """Base class for golden egg factory domain errors."""


class FoxAccessError(GoldenEggFactoryError):
    def __init__(self, actor: str) -> None:
        super().__init__(f"Factory access denied for {actor!r}")
        self.actor = actor


class InvalidEggCountError(GoldenEggFactoryError):
    def __init__(self, count_value: object) -> None:
        super().__init__(f"Egg count must be a positive integer, got {count_value!r}")
        self.count_value = count_value


class UnknownEggError(GoldenEggFactoryError):
    def __init__(self, egg_id: str) -> None:
        super().__init__(f"Unknown golden egg: {egg_id!r}")
        self.egg_id = egg_id


@dataclass(frozen=True)
class GoldenEgg:
    """A single egg produced by the protected factory."""

    egg_id: str
    owner: str
    value: int = GOLDEN_EGG_UNIT_VALUE
    karats: int = 24


@dataclass(frozen=True)
class FactoryValuation:
    """Current value report for the goose and its produced eggs."""

    goose_value: int
    egg_value: int
    egg_count: int

    @property
    def total_value(self) -> int:
        return self.goose_value + (self.egg_value * self.egg_count)


class GoldenEggFactory:
    """Produce and custody golden eggs without exposing the goose to foxes."""

    def __init__(
        self,
        *,
        authorized_keepers: set[str] | None = None,
        goose_value: int = GOOSE_INTRINSIC_VALUE,
        egg_value: int = GOLDEN_EGG_UNIT_VALUE,
    ) -> None:
        self._authorized_keepers = set(authorized_keepers or {"goose-keeper"})
        self._goose_value = goose_value
        self._egg_value = egg_value
        self._eggs: dict[str, GoldenEgg] = {}
        self._events: list[str] = []
        self._ids = count(1)

    def _require_keeper(self, actor: str) -> None:
        normalized = actor.strip().lower()
        if normalized == "fox" or actor not in self._authorized_keepers:
            self._events.append(f"blocked:{actor}")
            raise FoxAccessError(actor)

    def lay(self, actor: str, owner: str, count_value: int = 1) -> list[GoldenEgg]:
        """Create one or more golden eggs for ``owner``.

        Authorization and count validation both happen before mutation so a
        failed attempt never half-opens the factory door.
        """
        self._require_keeper(actor)
        if not isinstance(count_value, int) or count_value <= 0:
            raise InvalidEggCountError(count_value)

        produced: list[GoldenEgg] = []
        for _ in range(count_value):
            egg_id = f"golden-egg-{next(self._ids):04d}"
            egg = GoldenEgg(egg_id=egg_id, owner=owner, value=self._egg_value)
            self._eggs[egg_id] = egg
            produced.append(egg)
        self._events.append(f"laid:{actor}:{owner}:{len(produced)}")
        return produced

    def transfer(self, actor: str, egg_id: str, new_owner: str) -> GoldenEgg:
        """Transfer an existing egg while keeping factory access guarded."""
        self._require_keeper(actor)
        if egg_id not in self._eggs:
            raise UnknownEggError(egg_id)
        updated = GoldenEgg(
            egg_id=egg_id,
            owner=new_owner,
            value=self._eggs[egg_id].value,
            karats=self._eggs[egg_id].karats,
        )
        self._eggs[egg_id] = updated
        self._events.append(f"transferred:{actor}:{egg_id}:{new_owner}")
        return updated

    def valuation(self) -> FactoryValuation:
        return FactoryValuation(
            goose_value=self._goose_value,
            egg_value=self._egg_value,
            egg_count=len(self._eggs),
        )

    def list_eggs(self, actor: str) -> list[GoldenEgg]:
        self._require_keeper(actor)
        return list(self._eggs.values())

    def audit_events(self) -> list[str]:
        return list(self._events)
