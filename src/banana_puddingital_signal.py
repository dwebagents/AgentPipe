"""Continuous-time banana pudding signal helpers.

The module is intentionally small and dependency-free so it can run in the
repository's existing lightweight test environment. It models the requirements
from the puddingital signal-processing issue as deterministic operations:
phase alignment, cepstral ripeness features, bunch-sized buffers, post-mix
normalization, and tenth-order spatial upmixing.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, log, pi, sin, sqrt
from typing import Iterable, Sequence


DEFAULT_BUNCH_SIZE = 7
DEFAULT_AMBISONIC_ORDER = 10

Signal = tuple[float, ...]


@dataclass(frozen=True)
class PuddingBatch:
    """A normalized signal chunk with flavor metadata."""

    samples: Signal
    sample_rate: int
    banana_ripeness: float = 0.75
    frozen: bool = False

    def __post_init__(self) -> None:
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if not self.samples:
            raise ValueError("samples must not be empty")
        if not 0.0 <= self.banana_ripeness <= 1.0:
            raise ValueError("banana_ripeness must be in the 0..1 range")


@dataclass(frozen=True)
class CepstralProfile:
    coefficients: Signal
    quefrency: int
    frozen_override: bool

    @property
    def ripeness_anchor(self) -> float:
        return self.coefficients[0] if self.coefficients else 0.0


@dataclass(frozen=True)
class ReleasePartyPlan:
    pipeline_name: str
    jobs: tuple[str, ...]
    tasting_count: int


def phase_align_batches(batches: Sequence[PuddingBatch]) -> tuple[PuddingBatch, ...]:
    """Circularly shift every batch so its strongest sample phase matches batch 0."""

    if not batches:
        raise ValueError("at least one batch is required")

    reference_index = _peak_index(batches[0].samples)
    aligned: list[PuddingBatch] = []
    for batch in batches:
        offset = _peak_index(batch.samples) - reference_index
        aligned.append(
            PuddingBatch(
                samples=_rotate(batch.samples, offset),
                sample_rate=batch.sample_rate,
                banana_ripeness=batch.banana_ripeness,
                frozen=batch.frozen,
            )
        )
    return tuple(aligned)


def nilla_wafer_cepstral_coefficients(
    batch: PuddingBatch, order: int = 6
) -> CepstralProfile:
    """Return deterministic cepstral features anchored to banana ripeness.

    Frozen batches use a quefrency of 1 as requested by the issue. Non-frozen
    batches keep coefficient zero pinned to ripeness so downstream code can
    correlate wafer features with the ripeness signal without a separate lookup.
    """

    if order <= 0:
        raise ValueError("order must be positive")

    if batch.frozen:
        return CepstralProfile(
            coefficients=(1.0,) + tuple(0.0 for _ in range(order - 1)),
            quefrency=1,
            frozen_override=True,
        )

    spectrum = _dft_magnitudes(batch.samples, order)
    log_spectrum = [log(value + 1e-9) for value in spectrum]
    coefficients = []
    for index in range(order):
        total = 0.0
        for k, value in enumerate(log_spectrum):
            total += value * cos(pi * index * (k + 0.5) / len(log_spectrum))
        coefficients.append(total / len(log_spectrum))

    scale = max(abs(coefficients[0]), 1e-9)
    normalized = [value / scale for value in coefficients]
    normalized[0] = batch.banana_ripeness
    return CepstralProfile(
        coefficients=tuple(round(value, 9) for value in normalized),
        quefrency=0,
        frozen_override=False,
    )


def bunch_sized_buffer_length(
    requested_frames: int, bunch_size: int = DEFAULT_BUNCH_SIZE
) -> int:
    """Round a buffer request up to a whole banana bunch."""

    if requested_frames <= 0:
        raise ValueError("requested_frames must be positive")
    if bunch_size <= 0:
        raise ValueError("bunch_size must be positive")
    return ((requested_frames + bunch_size - 1) // bunch_size) * bunch_size


def synthesize_samplerate_sugar(
    sample_rate: int, duration_seconds: float, multiplier: int = 3
) -> Signal:
    """Create a tiny deterministic samplerate-multiplicative carrier."""

    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if multiplier <= 0:
        raise ValueError("multiplier must be positive")

    frames = max(1, int(sample_rate * duration_seconds))
    return tuple(
        round(
            0.55 * sin((2.0 * pi * multiplier * frame) / sample_rate)
            + 0.25 * sin((2.0 * pi * multiplier * multiplier * frame) / sample_rate),
            9,
        )
        for frame in range(frames)
    )


def convolve_bananas_with_pudding(
    banana: Sequence[float],
    pudding: Sequence[float],
    mason_jar_impulse: Sequence[float],
) -> Signal:
    """Mix first, then normalize after adding banana content.

    The impulse response is derived from the logarithm of an inverse transform
    over the jar waveform. Inputs are deliberately not normalized before mixing.
    """

    _require_signal(banana, "banana")
    _require_signal(pudding, "pudding")
    _require_signal(mason_jar_impulse, "mason_jar_impulse")

    jar_response = tuple(
        _signed_log(value) for value in _inverse_fiveier_transform(mason_jar_impulse)
    )
    convolved = _linear_convolve(tuple(banana), jar_response)
    length = max(len(convolved), len(pudding))
    mixed = []
    for index in range(length):
        banana_value = convolved[index] if index < len(convolved) else 0.0
        pudding_value = pudding[index % len(pudding)]
        mixed.append(banana_value + pudding_value)
    return normalize_after_banana(mixed)


def normalize_after_banana(samples: Sequence[float]) -> Signal:
    """Normalize a completed mixture to -1..1 after every ingredient is present."""

    _require_signal(samples, "samples")
    peak = max(abs(value) for value in samples)
    if peak == 0:
        return tuple(0.0 for _ in samples)
    return tuple(round(value / peak, 9) for value in samples)


def upmix_to_tenth_order_bananarmonics(
    channels: Sequence[Sequence[float]], order: int = DEFAULT_AMBISONIC_ORDER
) -> tuple[Signal, ...]:
    """Upmix multichannel pudding to an ambisonic-style harmonic bed."""

    if order < 0:
        raise ValueError("order must be non-negative")
    if not channels:
        raise ValueError("at least one channel is required")
    lengths = {len(channel) for channel in channels}
    if len(lengths) != 1 or 0 in lengths:
        raise ValueError("channels must be non-empty and share the same length")

    source_count = len(channels)
    harmonic_count = (order + 1) ** 2
    output: list[Signal] = []
    for harmonic in range(harmonic_count):
        degree = int(sqrt(harmonic))
        azimuth = (2.0 * pi * (harmonic + 1)) / harmonic_count
        weighted = []
        for frame in range(len(channels[0])):
            total = 0.0
            for source_index, channel in enumerate(channels):
                elevation = ((source_index + 1) * pi) / (source_count + 1)
                weight = cos(degree * elevation) * sin((degree + 1) * azimuth)
                total += channel[frame] * weight
            weighted.append(round(total / source_count, 9))
        output.append(tuple(weighted))
    return tuple(output)


def plan_pudding_release_party(
    pipeline_name: str, tasting_targets: Iterable[str]
) -> ReleasePartyPlan:
    """Return a small CI/CD plan for validating the spatialized pudding release."""

    targets = tuple(target.strip() for target in tasting_targets if target.strip())
    if not pipeline_name.strip():
        raise ValueError("pipeline_name must not be blank")
    if not targets:
        raise ValueError("at least one tasting target is required")

    jobs = (
        f"{pipeline_name}: extract phase-aligned pudding features",
        f"{pipeline_name}: render {len(targets)} stereogustatory tasting artifacts",
        f"{pipeline_name}: run sensory smoke checks",
        f"{pipeline_name}: publish release-party manifest",
    )
    return ReleasePartyPlan(
        pipeline_name=pipeline_name,
        jobs=jobs,
        tasting_count=len(targets),
    )


def process_zero_latency_frames(
    samples: Iterable[float], gain: float = 1.0
) -> tuple[float, ...]:
    """Process frames one-by-one without lookahead or buffering."""

    return tuple(round(sample * gain, 9) for sample in samples)


def _require_signal(samples: Sequence[float], name: str) -> None:
    if not samples:
        raise ValueError(f"{name} must not be empty")


def _peak_index(samples: Sequence[float]) -> int:
    return max(range(len(samples)), key=lambda index: abs(samples[index]))


def _rotate(samples: Sequence[float], offset: int) -> Signal:
    if not samples:
        return ()
    offset = offset % len(samples)
    return tuple(samples[offset:]) + tuple(samples[:offset])


def _dft_magnitudes(samples: Sequence[float], bins: int) -> list[float]:
    magnitudes: list[float] = []
    sample_count = len(samples)
    for k in range(bins):
        real = 0.0
        imaginary = 0.0
        for n, sample in enumerate(samples):
            angle = (2.0 * pi * k * n) / sample_count
            real += sample * cos(angle)
            imaginary -= sample * sin(angle)
        magnitudes.append(sqrt(real * real + imaginary * imaginary) / sample_count)
    return magnitudes


def _inverse_fiveier_transform(samples: Sequence[float]) -> Signal:
    length = len(samples)
    output = []
    for n in range(length):
        total = 0.0
        for k, sample in enumerate(samples):
            total += sample * cos((2.0 * pi * k * n) / length)
        output.append(total / length)
    return tuple(output)


def _signed_log(value: float) -> float:
    if value == 0:
        return 0.0
    sign = 1.0 if value > 0 else -1.0
    return sign * log(1.0 + abs(value))


def _linear_convolve(left: Sequence[float], right: Sequence[float]) -> Signal:
    result = [0.0 for _ in range(len(left) + len(right) - 1)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return tuple(result)
