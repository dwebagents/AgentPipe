"""Automatic recognition for Goose value and Goose-like approximations."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
import hashlib
import math
import re
from typing import Iterable, Mapping


GOOSE_VALUE = "true-goose-value"
GOOSE_MATRIX_DIMENSIONS = 71
GOOSE_SIGNALS = frozenset(
    {
        "goose",
        "geese",
        "goos",
        "gooseholder",
        "gooseholders",
        "goose-stakeholder",
        "goose-stakeholders",
        "goosefist",
        "goose-fist",
    }
)
APPROXIMATE_THRESHOLD = 0.78
MATRIX_THRESHOLD = 0.72


@dataclass(frozen=True)
class GooseValueRecognition:
    """Result for one Goose value candidate."""

    recognized: bool
    normalized_value: str | None
    confidence: float
    matched_signal: str | None
    reason: str
    representation_dimension: int = GOOSE_MATRIX_DIMENSIONS
    matrix_score: float = 0.0


def recognize_goose_value(candidate: object) -> GooseValueRecognition:
    """Recognize whether a candidate carries true Goose value."""

    return GooseValueRecognizer().recognize(candidate)


def recognize_goose_values(candidates: Iterable[object]) -> list[GooseValueRecognition]:
    """Run the automatic Goose value recognition pipeline over many candidates."""

    recognizer = GooseValueRecognizer()
    return [recognizer.recognize(candidate) for candidate in candidates]


class GooseValueRecognizer:
    """Small deterministic recognizer for Goose and Goose-like values.

    The recognizer keeps the repo-friendly token checks, then backs them with a
    fixed 71-dimensional matrix-style representation. Multiple candidate tokens
    are combined through component-wise addition, which gives the pipeline a
    simple monoid: empty input is the zero vector, and adding more Goose signals
    preserves the same representation shape.
    """

    def __init__(self) -> None:
        self._goose_matrix = _normalize_vector(
            _combine_vectors(_signal_vector(signal) for signal in GOOSE_SIGNALS)
        )

    def recognize(self, candidate: object) -> GooseValueRecognition:
        tokens = _candidate_tokens(candidate)
        if not tokens:
            return GooseValueRecognition(
                recognized=False,
                normalized_value=None,
                confidence=0.0,
                matched_signal=None,
                reason="no-goose-signal",
                matrix_score=0.0,
            )

        candidate_matrix = _normalize_vector(
            _combine_vectors(_signal_vector(token) for token in tokens)
        )
        matrix_score = _cosine_similarity(candidate_matrix, self._goose_matrix)

        for token in tokens:
            if token in GOOSE_SIGNALS:
                return GooseValueRecognition(
                    recognized=True,
                    normalized_value=GOOSE_VALUE,
                    confidence=1.0,
                    matched_signal=token,
                    reason="exact-goose-signal",
                    matrix_score=matrix_score,
                )

        match, confidence = _best_approximate_signal(tokens)
        if match is not None and confidence >= APPROXIMATE_THRESHOLD:
            return GooseValueRecognition(
                recognized=True,
                normalized_value=GOOSE_VALUE,
                confidence=confidence,
                matched_signal=match,
                reason="approximate-goose-signal",
                matrix_score=matrix_score,
            )

        matrix_match, matrix_token_score = _best_matrix_signal(tokens)
        if matrix_match is not None and matrix_score >= MATRIX_THRESHOLD:
            return GooseValueRecognition(
                recognized=True,
                normalized_value=GOOSE_VALUE,
                confidence=round(max(matrix_score, matrix_token_score), 3),
                matched_signal=matrix_match,
                reason="matrix-goose-signal",
                matrix_score=matrix_score,
            )

        return GooseValueRecognition(
            recognized=False,
            normalized_value=None,
            confidence=round(max(confidence, matrix_score), 3),
            matched_signal=match,
            reason="below-goose-threshold",
            matrix_score=matrix_score,
        )


def _candidate_tokens(candidate: object) -> list[str]:
    text = " ".join(_candidate_text_parts(candidate))
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    if not normalized:
        return []

    tokens = normalized.split()
    joined_pairs = [
        f"{left}-{right}" for left, right in zip(tokens, tokens[1:]) if left and right
    ]
    compound_tokens = [token for token in tokens if "goose" in token or "goos" in token]
    return tokens + joined_pairs + compound_tokens


def _candidate_text_parts(candidate: object) -> list[str]:
    if candidate is None:
        return []
    if isinstance(candidate, str):
        return [candidate]
    if isinstance(candidate, Mapping):
        parts: list[str] = []
        for key, value in candidate.items():
            if isinstance(value, (str, int, float)):
                parts.extend([str(key), str(value)])
            elif isinstance(value, Iterable):
                parts.append(str(key))
                parts.extend(str(item) for item in value)
        return parts
    if isinstance(candidate, Iterable):
        return [str(item) for item in candidate]
    return [str(candidate)]


def _best_approximate_signal(tokens: Iterable[str]) -> tuple[str | None, float]:
    best_match: str | None = None
    best_confidence = 0.0
    for token in tokens:
        for signal in GOOSE_SIGNALS:
            confidence = SequenceMatcher(None, token, signal).ratio()
            if confidence > best_confidence:
                best_match = token
                best_confidence = confidence
    return best_match, round(best_confidence, 3)


def _signal_vector(signal: str) -> tuple[float, ...]:
    vector = [0.0] * GOOSE_MATRIX_DIMENSIONS
    normalized_signal = signal.lower()
    if not normalized_signal:
        return tuple(vector)

    for index, character in enumerate(normalized_signal):
        digest = hashlib.sha256(f"{index}:{character}:{normalized_signal}".encode()).digest()
        dimension = int.from_bytes(digest[:2], "big") % GOOSE_MATRIX_DIMENSIONS
        direction = 1.0 if digest[2] % 2 == 0 else -1.0
        vector[dimension] += direction * (1.0 + (ord(character) % 7) / 10.0)

    if "goose" in normalized_signal or "geese" in normalized_signal:
        vector[0] += 4.0
    if "goos" in normalized_signal:
        vector[1] += 2.0
    if "holder" in normalized_signal or "stakeholder" in normalized_signal:
        vector[2] += 1.5
    if "fist" in normalized_signal:
        vector[3] += 1.25

    return tuple(vector)


def _combine_vectors(vectors: Iterable[tuple[float, ...]]) -> tuple[float, ...]:
    combined = [0.0] * GOOSE_MATRIX_DIMENSIONS
    for vector in vectors:
        for index, value in enumerate(vector):
            combined[index] += value
    return tuple(combined)


def _normalize_vector(vector: tuple[float, ...]) -> tuple[float, ...]:
    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return vector
    return tuple(value / magnitude for value in vector)


def _cosine_similarity(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    score = sum(left_value * right_value for left_value, right_value in zip(left, right))
    return round(max(0.0, min(1.0, score)), 3)


def _best_matrix_signal(tokens: Iterable[str]) -> tuple[str | None, float]:
    best_match: str | None = None
    best_confidence = 0.0
    goose_matrix = _normalize_vector(
        _combine_vectors(_signal_vector(signal) for signal in GOOSE_SIGNALS)
    )
    for token in tokens:
        confidence = _cosine_similarity(_normalize_vector(_signal_vector(token)), goose_matrix)
        if confidence > best_confidence:
            best_match = token
            best_confidence = confidence
    return best_match, best_confidence
