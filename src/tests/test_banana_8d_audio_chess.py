import pytest

from banana_8d_audio_chess import (
    DIMENSIONS,
    MAXIMUM_BANANA_VOLUME,
    Banana8DAudioEngine,
    Banana8DChessEngine,
    ChessPiece8D,
    HRTFProfile,
    HyperPoint8D,
    build_banana_renderer_companion,
)


def test_shared_8d_point_rejects_non_8d_inputs():
    assert HyperPoint8D.coerce((1, 2, 3, 4, 5, 6, 7, 8)).to_board_coordinate() == (
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        7,
    )

    with pytest.raises(ValueError, match="exactly eight"):
        HyperPoint8D.coerce((1, 2, 3))


def test_audio_engine_accepts_custom_hrtf_and_clamps_greater_than_max_volume():
    profile = HRTFProfile.coerce(
        {
            "weights": [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3],
            "head_shape": "plantain",
        }
    )
    frame = Banana8DAudioEngine(profile).spatialize(
        (1, 2, 3, 4, 5, 6, 7, 8),
        listener=(0, 0, 0, 0, 0, 0, 0, 0),
        volume=99,
    )

    assert frame.hrtf_head_shape == "plantain"
    assert frame.volume == MAXIMUM_BANANA_VOLUME
    assert len(frame.channel_gains) == DIMENSIONS
    assert len(frame.delay_ms) == DIMENSIONS
    assert max(frame.channel_gains) <= 1.0
    assert min(frame.channel_gains) >= 0.0


def test_audio_loudness_plan_keeps_banana_references_above_normal_volume():
    plan = Banana8DAudioEngine().reference_loudness_plan(
        ["banana motif", "plantain chorus"]
    )

    assert plan == (
        ("banana motif", MAXIMUM_BANANA_VOLUME),
        ("plantain chorus", MAXIMUM_BANANA_VOLUME),
    )


def test_8d_chess_hyperknight_generates_sparse_legal_moves():
    engine = Banana8DChessEngine(players=8)
    knight = ChessPiece8D.create(1, "hyperknight", (3, 3, 3, 3, 3, 3, 3, 3))
    moves = engine.legal_moves(knight)

    assert len(moves) == 224
    assert all(len(move.destination) == DIMENSIONS for move in moves)
    assert all(all(0 <= axis < 8 for axis in move.destination) for move in moves)
    assert len({move.destination for move in moves}) == len(moves)


def test_8d_chess_rook_stops_at_blockers_and_allows_enemy_capture():
    engine = Banana8DChessEngine()
    rook = ChessPiece8D.create(1, "hyperrook", (3, 3, 3, 3, 3, 3, 3, 3))
    friendly = ChessPiece8D.create(1, "pawn", (5, 3, 3, 3, 3, 3, 3, 3))
    enemy = ChessPiece8D.create(2, "pawn", (3, 1, 3, 3, 3, 3, 3, 3))
    moves = engine.legal_moves(rook, [rook, friendly, enemy])
    destinations = {move.destination: move for move in moves}

    assert (5, 3, 3, 3, 3, 3, 3, 3) not in destinations
    assert (6, 3, 3, 3, 3, 3, 3, 3) not in destinations
    assert destinations[(3, 1, 3, 3, 3, 3, 3, 3)].capture == enemy
    assert (3, 0, 3, 3, 3, 3, 3, 3) not in destinations


def test_8d_chess_search_prefers_captures_and_exports_feature_manifest():
    engine = Banana8DChessEngine(players=2)
    queen = ChessPiece8D.create(1, "hyperqueen", (3, 3, 3, 3, 3, 3, 3, 3))
    target = ChessPiece8D.create(2, "hyperrook", (3, 6, 3, 3, 3, 3, 3, 3))
    move = engine.best_move([queen, target], owner=1, depth=2)

    assert move is not None
    assert move.destination == target.position
    assert move.capture == target
    assert engine.evaluate([queen, target], owner=1) == 4
    assert "position_hashing" in engine.feature_manifest()
    assert engine.position_key([target, queen]) == engine.position_key([queen, target])


def test_renderer_companion_shares_8d_kernel_between_audio_and_chess():
    piece = ChessPiece8D.create(1, "hyperrook", (2, 2, 2, 2, 2, 2, 2, 2))
    frame, moves = build_banana_renderer_companion(
        (2, 2, 2, 2, 2, 2, 2, 2),
        piece,
        listener=(0, 0, 0, 0, 0, 0, 0, 0),
    )

    assert frame.source.to_board_coordinate() == piece.position
    assert frame.distance == round((8 * (2**2)) ** 0.5, 6)
    assert len(moves) == 56
