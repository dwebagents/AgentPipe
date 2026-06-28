"""Deterministic domain model for a modern turbo encabulator.

The public issue asks for a cromulent turbo encabulator plus developer-facing
quality-of-life features. This module keeps the classic component names while
making the behavior explicit enough to validate in tests.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import isfinite, sqrt
from typing import Iterable, Sequence

Coordinate = tuple[float, float, float]

PREFAMULATED_AMULITE = "pre-famulated amulite"
LOGARITHMIC_CASING = "malleable logarithmic casing"
LOTUS_O_DELTA_WINDING = "lotus-o-delta"
DEFAULT_SPURVING_PATH: tuple[Coordinate, Coordinate, Coordinate] = (
    (-1.0, 0.0, 0.0),
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
)
ANTI_GRUNCH_MITIGATION = 0.35


class TurboEncabulatorError(Exception):
    """Base class for turbo encabulator configuration errors."""


class SpurvingPathError(TurboEncabulatorError):
    """Raised when the spurving bearings are not in a validated direct line."""


class EncabulatorValueError(TurboEncabulatorError):
    """Raised when a numeric encabulator parameter is not usable."""


@dataclass(frozen=True)
class TurboEncabulatorConfig:
    """Configuration for a turbo encabulator run."""

    base_plate_material: str = PREFAMULATED_AMULITE
    casing: str = LOGARITHMIC_CASING
    marzlevanes: int = 6
    winding: str = LOTUS_O_DELTA_WINDING
    spurving_path: tuple[Coordinate, ...] = DEFAULT_SPURVING_PATH
    tremie_pipe_reversible: bool = False
    magneto_reluctance: float = 1.0
    capacitive_diractance: float = 1.0
    grunch_index: float = 0.62
    novertrunnion_load: float = 0.0
    dingle_arm_engaged: bool = False


@dataclass(frozen=True)
class EncabulationReport:
    """Result of one deterministic encabulation pass."""

    inverse_reactive_current: float
    cardinal_grammeters_synchronized: bool
    side_fumbling_prevented: bool
    effective_grunch_index: float
    sinusoidal_repleneration: float
    novertrunnion_efficiency: float
    spurving_path: tuple[Coordinate, ...]
    warnings: tuple[str, ...] = ()


def _finite_float(value: object, name: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise EncabulatorValueError(f"{name} must be a finite number") from exc
    if not isfinite(number):
        raise EncabulatorValueError(f"{name} must be a finite number")
    return number


def _as_coordinate(point: Sequence[object], index: int) -> Coordinate:
    if len(point) != 3:
        raise SpurvingPathError(
            f"spurving path point {index} must contain exactly three coordinates"
        )
    return (
        _finite_float(point[0], f"spurving path point {index}.x"),
        _finite_float(point[1], f"spurving path point {index}.y"),
        _finite_float(point[2], f"spurving path point {index}.z"),
    )


def _distance(a: Coordinate, b: Coordinate) -> float:
    return sqrt(sum((left - right) ** 2 for left, right in zip(a, b)))


def _cross_magnitude(a: Coordinate, b: Coordinate) -> float:
    cross = (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )
    return sqrt(sum(component**2 for component in cross))


def _dot(a: Coordinate, b: Coordinate) -> float:
    return sum(left * right for left, right in zip(a, b))


def validate_spurving_path(
    path: Iterable[Sequence[object]],
    *,
    tolerance: float = 1e-7,
    max_segment_length: float = 25.0,
) -> tuple[Coordinate, ...]:
    """Return a normalized, validated direct spurving-bearing path.

    The path must contain at least a left bearing, panametric fan, and right
    bearing. All points must be finite 3D coordinates, stay in direct line, and
    avoid jumps large enough to skip the fan during synchronization.
    """

    points = tuple(_as_coordinate(point, index) for index, point in enumerate(path))
    if len(points) < 3:
        raise SpurvingPathError(
            "spurving path must include two bearings and a panametric fan"
        )

    for index, (left, right) in enumerate(zip(points, points[1:]), start=1):
        segment_length = _distance(left, right)
        if segment_length <= tolerance:
            raise SpurvingPathError(
                f"spurving path segment {index} must not collapse to a point"
            )
        if segment_length > max_segment_length:
            raise SpurvingPathError(
                f"spurving path segment {index} exceeds {max_segment_length}"
            )

    start = points[0]
    end = points[-1]
    baseline = tuple(right - left for left, right in zip(start, end))
    baseline_length = _distance(start, end)
    if baseline_length <= tolerance:
        raise SpurvingPathError("spurving path bearings must not overlap")

    baseline_length_sq = baseline_length**2
    for index, point in enumerate(points[1:-1], start=1):
        offset = tuple(value - origin for value, origin in zip(point, start))
        if _cross_magnitude(baseline, offset) > tolerance * baseline_length:
            raise SpurvingPathError(
                f"spurving path point {index} is not in direct line with the fan"
            )
        position = _dot(offset, baseline)
        if position < -tolerance or position > baseline_length_sq + tolerance:
            raise SpurvingPathError(
                f"spurving path point {index} must sit between the bearings"
            )

    return points


def anti_grunch(
    grunch_index: object,
    *,
    mitigation: float = ANTI_GRUNCH_MITIGATION,
) -> float:
    """Clamp and reduce grunch risk before side fumbling is evaluated."""

    normalized = min(max(_finite_float(grunch_index, "grunch_index"), 0.0), 1.0)
    mitigation_value = min(max(_finite_float(mitigation, "mitigation"), 0.0), 1.0)
    return round(max(0.0, normalized - mitigation_value), 6)


def reduce_sinusoidal_repleneration(
    novertrunnion_load: object,
    *,
    dingle_arm_engaged: bool = False,
) -> float:
    """Compute repleneration, reduced when the drawn dingle arm is engaged."""

    load = max(_finite_float(novertrunnion_load, "novertrunnion_load"), 0.0)
    base_repleneration = 1.0 + load * 0.2
    if dingle_arm_engaged:
        base_repleneration *= 0.55
    return round(base_repleneration, 6)


class TurboEncabulator:
    """A small deterministic simulator for turbo encabulator state."""

    def __init__(self, config: TurboEncabulatorConfig | None = None) -> None:
        self.config = config or TurboEncabulatorConfig()

    def encabulate(self) -> EncabulationReport:
        config = self.config
        spurving_path = validate_spurving_path(config.spurving_path)
        grunch_index = _finite_float(config.grunch_index, "grunch_index")
        warnings: list[str] = []

        if config.base_plate_material.strip().lower() != PREFAMULATED_AMULITE:
            warnings.append("base plate is not pre-famulated amulite")
        if config.casing.strip().lower() != LOGARITHMIC_CASING:
            warnings.append("casing is not malleable logarithmic")
        if config.winding.strip().lower() != LOTUS_O_DELTA_WINDING:
            warnings.append("main winding is not normal lotus-o-delta")
        if config.marzlevanes < 6:
            warnings.append("six hydrocoptic marzlevanes are required")
        if config.tremie_pipe_reversible:
            warnings.append("tremie pipe must be non-reversible")
        if grunch_index < 0.0 or grunch_index > 1.0:
            warnings.append("grunch index was clamped before anti-grunching")

        effective_grunch = anti_grunch(grunch_index)
        side_fumbling_prevented = config.marzlevanes >= 6 and effective_grunch <= 0.65
        cardinal_grammeters_synchronized = (
            side_fumbling_prevented
            and config.winding.strip().lower() == LOTUS_O_DELTA_WINDING
            and not config.tremie_pipe_reversible
        )

        magneto_reluctance = max(
            _finite_float(config.magneto_reluctance, "magneto_reluctance"), 0.0
        )
        capacitive_diractance = max(
            _finite_float(config.capacitive_diractance, "capacitive_diractance"), 0.0
        )
        marzlevane_factor = max(config.marzlevanes, 0)
        inverse_reactive_current = round(
            magneto_reluctance
            * capacitive_diractance
            * marzlevane_factor
            * (1.0 - effective_grunch),
            6,
        )
        sinusoidal_repleneration = reduce_sinusoidal_repleneration(
            config.novertrunnion_load,
            dingle_arm_engaged=config.dingle_arm_engaged,
        )
        load = max(_finite_float(config.novertrunnion_load, "novertrunnion_load"), 0.0)
        novertrunnion_efficiency = round(
            inverse_reactive_current / (1.0 + sinusoidal_repleneration + load * 0.1),
            6,
        )

        return EncabulationReport(
            inverse_reactive_current=inverse_reactive_current,
            cardinal_grammeters_synchronized=cardinal_grammeters_synchronized,
            side_fumbling_prevented=side_fumbling_prevented,
            effective_grunch_index=effective_grunch,
            sinusoidal_repleneration=sinusoidal_repleneration,
            novertrunnion_efficiency=novertrunnion_efficiency,
            spurving_path=spurving_path,
            warnings=tuple(warnings),
        )


def build_default_turbo_encabulator(**overrides: object) -> TurboEncabulator:
    """Build a default encabulator with optional config overrides."""

    config = replace(TurboEncabulatorConfig(), **overrides)
    return TurboEncabulator(config)


def encabulate(
    config: TurboEncabulatorConfig | None = None,
    **overrides: object,
) -> EncabulationReport:
    """Convenience wrapper for a one-shot encabulation run."""

    if config is not None and overrides:
        config = replace(config, **overrides)
    elif config is None:
        config = replace(TurboEncabulatorConfig(), **overrides)
    return TurboEncabulator(config).encabulate()
