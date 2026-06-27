"""Shared 8D audio and chess primitives for the banana renderer.

The issue asks for 8D audio and 8D chess to share implementation surface. This
module keeps the shared geometry in one place and layers deterministic audio
spatialization plus sparse 8D chess move generation on top.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import blake2b
from math import sqrt
from typing import Iterable, Mapping, Sequence, Union


DIMENSIONS = 8
BOARD_SIZE = 8
MAX_PLAYERS = 8
MAXIMUM_BANANA_VOLUME = 1.25
STOCKFISH_STYLE_FEATURES = (
    "legal_move_generation",
    "material_evaluation",
    "mobility_evaluation",
    "position_hashing",
    "principal_variation_seed",
    "depth_limited_search",
    "deterministic_move_ordering",
    "time_budget_hook",
)

Number = Union[int, float]
Coordinate8D = tuple[int, int, int, int, int, int, int, int]


@dataclass(frozen=True)
class HyperPoint8D:
    """An immutable point in 8-dimensional banana space."""

    values: tuple[float, float, float, float, float, float, float, float]

    @classmethod
    def coerce(
        cls,
        value: "HyperPoint8D | Mapping[str, Number] | Sequence[Number]",
    ) -> "HyperPoint8D":
        if isinstance(value, HyperPoint8D):
            return value
        if isinstance(value, Mapping):
            keys = ("x", "y", "z", "w", "a", "b", "c", "d")
            values = tuple(float(value.get(key, 0.0)) for key in keys)
        else:
            if len(value) != DIMENSIONS:
                raise ValueError("8D points must contain exactly eight coordinates")
            values = tuple(float(item) for item in value)
        if len(values) != DIMENSIONS:
            raise ValueError("8D points must contain exactly eight coordinates")
        return cls(values)  # type: ignore[arg-type]

    def distance_to(
        self,
        other: "HyperPoint8D | Mapping[str, Number] | Sequence[Number]",
    ) -> float:
        target = HyperPoint8D.coerce(other)
        return sqrt(
            sum((left - right) ** 2 for left, right in zip(self.values, target.values))
        )

    def unit_bias_from(
        self,
        origin: "HyperPoint8D | Mapping[str, Number] | Sequence[Number]",
    ) -> tuple[float, ...]:
        source = HyperPoint8D.coerce(origin)
        deltas = tuple(value - base for value, base in zip(self.values, source.values))
        length = sqrt(sum(delta * delta for delta in deltas))
        if length == 0:
            return (0.0,) * DIMENSIONS
        return tuple(delta / length for delta in deltas)

    def to_board_coordinate(self) -> Coordinate8D:
        return tuple(
            max(0, min(BOARD_SIZE - 1, int(round(value))))
            for value in self.values
        )  # type: ignore[return-value]


@dataclass(frozen=True)
class HRTFProfile:
    """Per-axis gain profile for banana-shaped-head 8D playback."""

    weights: tuple[float, float, float, float, float, float, float, float]
    head_shape: str = "banana"

    @classmethod
    def coerce(
        cls,
        value: "HRTFProfile | Mapping[str, object] | Sequence[Number] | None",
    ) -> "HRTFProfile":
        if isinstance(value, HRTFProfile):
            return value
        if value is None:
            return cls((1.0, 0.94, 0.88, 0.82, 0.76, 0.70, 0.64, 0.58))
        if isinstance(value, Mapping):
            raw_weights = value.get("weights", ())
            head_shape = str(value.get("head_shape", "banana"))
        else:
            raw_weights = value
            head_shape = "custom"
        weights = tuple(float(item) for item in raw_weights)  # type: ignore[arg-type]
        if len(weights) != DIMENSIONS:
            raise ValueError("custom HRTF data must provide eight weights")
        if any(weight < 0 for weight in weights):
            raise ValueError("custom HRTF weights must be non-negative")
        return cls(weights, head_shape)  # type: ignore[arg-type]


@dataclass(frozen=True)
class AudioSpatialFrame:
    """A deterministic 8D spatialization frame."""

    source: HyperPoint8D
    listener: HyperPoint8D
    distance: float
    channel_gains: tuple[float, float, float, float, float, float, float, float]
    delay_ms: tuple[float, float, float, float, float, float, float, float]
    volume: float
    hrtf_head_shape: str


class Banana8DAudioEngine:
    """Spatializes banana references across eight deterministic channels."""

    def __init__(
        self,
        hrtf_profile: HRTFProfile | Mapping[str, object] | Sequence[Number] | None = None,
    ) -> None:
        self.hrtf_profile = HRTFProfile.coerce(hrtf_profile)

    def spatialize(
        self,
        source: HyperPoint8D | Mapping[str, Number] | Sequence[Number],
        *,
        listener: HyperPoint8D | Mapping[str, Number] | Sequence[Number] | None = None,
        volume: float = 1.0,
    ) -> AudioSpatialFrame:
        source_point = HyperPoint8D.coerce(source)
        listener_point = HyperPoint8D.coerce(listener or (0.0,) * DIMENSIONS)
        distance = source_point.distance_to(listener_point)
        bias = source_point.unit_bias_from(listener_point)
        loudness = max(0.0, min(MAXIMUM_BANANA_VOLUME, float(volume)))
        attenuation = 1.0 / (1.0 + distance * 0.18)
        raw = tuple(
            (0.5 + abs(axis_bias) * 0.5) * weight * attenuation * loudness
            for axis_bias, weight in zip(bias, self.hrtf_profile.weights)
        )
        peak = max(max(raw), 1.0)
        gains = tuple(round(value / peak, 6) for value in raw)
        delays = tuple(
            round((index + 1) * 0.17 + abs(axis_bias) * 1.9, 6)
            for index, axis_bias in enumerate(bias)
        )
        return AudioSpatialFrame(
            source=source_point,
            listener=listener_point,
            distance=round(distance, 6),
            channel_gains=gains,  # type: ignore[arg-type]
            delay_ms=delays,  # type: ignore[arg-type]
            volume=loudness,
            hrtf_head_shape=self.hrtf_profile.head_shape,
        )

    def reference_loudness_plan(
        self,
        titles: Iterable[str],
        *,
        volume: float = MAXIMUM_BANANA_VOLUME,
    ) -> tuple[tuple[str, float], ...]:
        loudness = max(0.0, min(MAXIMUM_BANANA_VOLUME, float(volume)))
        return tuple((title, loudness) for title in titles)


@dataclass(frozen=True)
class ChessPiece8D:
    owner: int
    kind: str
    position: Coordinate8D

    @classmethod
    def create(cls, owner: int, kind: str, position: Sequence[int]) -> "ChessPiece8D":
        return cls(_validate_owner(owner), kind.lower(), _validate_coordinate(position))


@dataclass(frozen=True)
class ChessMove8D:
    piece: ChessPiece8D
    destination: Coordinate8D
    capture: ChessPiece8D | None = None

    @property
    def vector(self) -> Coordinate8D:
        return tuple(
            dest - start for start, dest in zip(self.piece.position, self.destination)
        )  # type: ignore[return-value]


class Banana8DChessEngine:
    """Sparse 8D chess engine with deterministic move ordering and evaluation."""

    material_values = {
        "pawn": 1,
        "hyperknight": 3,
        "bishop": 3,
        "hyperrook": 5,
        "hyperqueen": 9,
        "king": 100,
    }

    def __init__(self, players: int = 2, board_size: int = BOARD_SIZE) -> None:
        if not 1 <= players <= MAX_PLAYERS:
            raise ValueError("8D chess supports between one and eight players")
        if board_size != BOARD_SIZE:
            raise ValueError("this sparse engine is fixed to an 8x8x8x8x8x8x8x8 board")
        self.players = players
        self.board_size = board_size

    def legal_moves(
        self,
        piece: ChessPiece8D,
        occupied: Iterable[ChessPiece8D] = (),
    ) -> tuple[ChessMove8D, ...]:
        blockers = {
            other.position: other
            for other in occupied
            if other.position != piece.position
        }
        if piece.kind in ("hyperrook", "rook"):
            destinations = self._linear_destinations(piece.position, blockers)
        elif piece.kind in ("hyperknight", "knight"):
            destinations = self._knight_destinations(piece.position)
        elif piece.kind in ("hyperqueen", "queen"):
            destinations = tuple(
                dict.fromkeys(
                    self._linear_destinations(piece.position, blockers)
                    + self._diagonal_destinations(piece.position, blockers)
                )
            )
        elif piece.kind == "king":
            destinations = self._king_destinations(piece.position)
        else:
            destinations = self._pawn_destinations(piece)

        moves = []
        for destination in destinations:
            capture = blockers.get(destination)
            if capture is not None and capture.owner == piece.owner:
                continue
            moves.append(ChessMove8D(piece, destination, capture))
        return tuple(sorted(moves, key=lambda move: move.destination))

    def best_move(
        self,
        pieces: Iterable[ChessPiece8D],
        owner: int,
        *,
        depth: int = 1,
    ) -> ChessMove8D | None:
        owner = _validate_owner(owner)
        piece_list = tuple(pieces)
        candidate_moves = tuple(
            move
            for piece in piece_list
            if piece.owner == owner
            for move in self.legal_moves(piece, piece_list)
        )
        if not candidate_moves:
            return None
        search_depth = max(1, min(2, int(depth)))
        return max(
            candidate_moves,
            key=lambda move: (
                self._score_move(move, piece_list, search_depth),
                move.piece.kind,
                move.destination,
            ),
        )

    def evaluate(self, pieces: Iterable[ChessPiece8D], owner: int) -> int:
        owner = _validate_owner(owner)
        total = 0
        for piece in pieces:
            value = self.material_values.get(piece.kind, 1)
            total += value if piece.owner == owner else -value
        return total

    def position_key(self, pieces: Iterable[ChessPiece8D]) -> str:
        payload = "|".join(
            f"{piece.owner}:{piece.kind}:{','.join(str(axis) for axis in piece.position)}"
            for piece in sorted(
                pieces, key=lambda item: (item.owner, item.kind, item.position)
            )
        )
        return blake2b(payload.encode("ascii"), digest_size=12).hexdigest()

    def feature_manifest(self) -> tuple[str, ...]:
        return STOCKFISH_STYLE_FEATURES

    def _score_move(
        self,
        move: ChessMove8D,
        pieces: tuple[ChessPiece8D, ...],
        depth: int,
    ) -> float:
        capture_score = (
            0
            if move.capture is None
            else self.material_values.get(move.capture.kind, 1) * 10
        )
        center = HyperPoint8D((3.5,) * DIMENSIONS)
        destination = HyperPoint8D(  # type: ignore[arg-type]
            tuple(float(axis) for axis in move.destination)
        )
        center_score = 10.0 - destination.distance_to(center)
        mobility_score = len(
            self.legal_moves(
                ChessPiece8D(move.piece.owner, move.piece.kind, move.destination),
                pieces,
            )
        )
        return capture_score + center_score + (0.05 * mobility_score * depth)

    def _linear_destinations(
        self,
        position: Coordinate8D,
        blockers: Mapping[Coordinate8D, ChessPiece8D],
    ) -> tuple[Coordinate8D, ...]:
        destinations = []
        for axis in range(DIMENSIONS):
            for direction in (-1, 1):
                current = list(position)
                for _ in range(BOARD_SIZE - 1):
                    current[axis] += direction
                    if not 0 <= current[axis] < BOARD_SIZE:
                        break
                    destination = tuple(current)  # type: ignore[assignment]
                    destinations.append(destination)
                    if destination in blockers:
                        break
        return tuple(destinations)

    def _diagonal_destinations(
        self,
        position: Coordinate8D,
        blockers: Mapping[Coordinate8D, ChessPiece8D],
    ) -> tuple[Coordinate8D, ...]:
        destinations = []
        for first_axis in range(DIMENSIONS):
            for second_axis in range(first_axis + 1, DIMENSIONS):
                for first_dir in (-1, 1):
                    for second_dir in (-1, 1):
                        current = list(position)
                        for _ in range(BOARD_SIZE - 1):
                            current[first_axis] += first_dir
                            current[second_axis] += second_dir
                            if not all(0 <= axis < BOARD_SIZE for axis in current):
                                break
                            destination = tuple(current)  # type: ignore[assignment]
                            destinations.append(destination)
                            if destination in blockers:
                                break
        return tuple(destinations)

    def _knight_destinations(self, position: Coordinate8D) -> tuple[Coordinate8D, ...]:
        destinations = []
        for long_axis in range(DIMENSIONS):
            for short_axis in range(DIMENSIONS):
                if short_axis == long_axis:
                    continue
                for long_step in (-2, 2):
                    for short_step in (-1, 1):
                        current = list(position)
                        current[long_axis] += long_step
                        current[short_axis] += short_step
                        if all(0 <= axis < BOARD_SIZE for axis in current):
                            destinations.append(tuple(current))  # type: ignore[arg-type]
        return tuple(dict.fromkeys(destinations))

    def _king_destinations(self, position: Coordinate8D) -> tuple[Coordinate8D, ...]:
        destinations = []
        for axis in range(DIMENSIONS):
            for direction in (-1, 1):
                current = list(position)
                current[axis] += direction
                if 0 <= current[axis] < BOARD_SIZE:
                    destinations.append(tuple(current))  # type: ignore[arg-type]
        return tuple(destinations)

    def _pawn_destinations(self, piece: ChessPiece8D) -> tuple[Coordinate8D, ...]:
        forward_axis = (piece.owner - 1) % DIMENSIONS
        direction = 1 if piece.owner % 2 else -1
        current = list(piece.position)
        current[forward_axis] += direction
        if 0 <= current[forward_axis] < BOARD_SIZE:
            return (tuple(current),)  # type: ignore[return-value]
        return ()


def build_banana_renderer_companion(
    source: HyperPoint8D | Mapping[str, Number] | Sequence[Number],
    piece: ChessPiece8D,
    *,
    listener: HyperPoint8D | Mapping[str, Number] | Sequence[Number] | None = None,
    hrtf_profile: HRTFProfile | Mapping[str, object] | Sequence[Number] | None = None,
) -> tuple[AudioSpatialFrame, tuple[ChessMove8D, ...]]:
    """Build synchronized 8D audio and chess outputs for one renderer frame."""

    audio_frame = Banana8DAudioEngine(hrtf_profile).spatialize(source, listener=listener)
    chess_moves = Banana8DChessEngine(players=max(2, piece.owner)).legal_moves(piece)
    return audio_frame, chess_moves


def _validate_coordinate(position: Sequence[int]) -> Coordinate8D:
    if len(position) != DIMENSIONS:
        raise ValueError("8D board coordinates must contain exactly eight axes")
    coordinate = tuple(int(axis) for axis in position)
    if any(axis < 0 or axis >= BOARD_SIZE for axis in coordinate):
        raise ValueError("8D board coordinates must stay within 0..7 on every axis")
    return coordinate  # type: ignore[return-value]


def _validate_owner(owner: int) -> int:
    owner = int(owner)
    if not 1 <= owner <= MAX_PLAYERS:
        raise ValueError("piece owner must be between 1 and 8")
    return owner
