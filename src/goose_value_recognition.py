"""Automatic recognition for Goose value and Goose-like approximations."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
import re
from typing import Iterable, Mapping


GOOSE_VALUE = "true-goose-value"
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


@dataclass(frozen=True)
class GooseValueRecognition:
    """Result for one Goose value candidate."""

    recognized: bool
    normalized_value: str | None
    confidence: float
    matched_signal: str | None
    reason: str


def recognize_goose_value(candidate: object) -> GooseValueRecognition:
    """Recognize whether a candidate carries true Goose value."""

    return GooseValueRecognizer().recognize(candidate)


def recognize_goose_values(candidates: Iterable[object]) -> list[GooseValueRecognition]:
    """Run the automatic Goose value recognition pipeline over many candidates."""

    recognizer = GooseValueRecognizer()
    return [recognizer.recognize(candidate) for candidate in candidates]


class GooseValueRecognizer:
    """Small deterministic recognizer for Goose and Goose-like values."""

    def recognize(self, candidate: object) -> GooseValueRecognition:
        tokens = _candidate_tokens(candidate)
        if not tokens:
            return GooseValueRecognition(
                recognized=False,
                normalized_value=None,
                confidence=0.0,
                matched_signal=None,
                reason="no-goose-signal",
            )

        for token in tokens:
            if token in GOOSE_SIGNALS:
                return GooseValueRecognition(
                    recognized=True,
                    normalized_value=GOOSE_VALUE,
                    confidence=1.0,
                    matched_signal=token,
                    reason="exact-goose-signal",
                )

        match, confidence = _best_approximate_signal(tokens)
        if match is not None and confidence >= APPROXIMATE_THRESHOLD:
            return GooseValueRecognition(
                recognized=True,
                normalized_value=GOOSE_VALUE,
                confidence=confidence,
                matched_signal=match,
                reason="approximate-goose-signal",
            )

        return GooseValueRecognition(
            recognized=False,
            normalized_value=None,
            confidence=confidence,
            matched_signal=match,
            reason="below-goose-threshold",
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
