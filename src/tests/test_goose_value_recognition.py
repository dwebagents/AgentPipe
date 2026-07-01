from goose_value_recognition import (
    GOOSE_MATRIX_DIMENSIONS,
    GOOSE_VALUE,
    GooseValueRecognizer,
    recognize_goose_value,
    recognize_goose_values,
)


def test_exact_goose_value_is_recognized():
    result = recognize_goose_value("true Goose value")

    assert result.recognized is True
    assert result.normalized_value == GOOSE_VALUE
    assert result.confidence == 1.0
    assert result.matched_signal == "goose"
    assert result.reason == "exact-goose-signal"
    assert result.representation_dimension == GOOSE_MATRIX_DIMENSIONS
    assert result.matrix_score > 0.0


def test_approximate_goose_value_is_recognized():
    result = recognize_goose_value("automatic gooze value recognision")

    assert result.recognized is True
    assert result.normalized_value == GOOSE_VALUE
    assert result.confidence >= 0.78
    assert result.matched_signal == "gooze"
    assert result.reason == "approximate-goose-signal"


def test_nearby_bird_value_candidates_are_recognized():
    results = recognize_goose_values(
        [
            "ducks with golden egg factory capacities",
            "pigeons sold as value-bearing egg generators",
            {"description": "other birds might implement egg factory capacity"},
        ]
    )

    assert [result.recognized for result in results] == [True, True, True]
    assert [result.reason for result in results] == [
        "approximate-goose-value-signal",
        "approximate-goose-value-signal",
        "approximate-goose-value-signal",
    ]
    assert results[0].matched_signal == "ducks"
    assert results[1].matched_signal == "pigeons"
    assert results[2].matched_signal == "birds"
    assert results[0].confidence >= 0.88


def test_structured_candidate_fields_are_scanned():
    candidate = {
        "name": "Stakeholder packet",
        "description": "Preserve value for short Gooseholders",
        "tags": ["pipeline", "value"],
    }

    result = GooseValueRecognizer().recognize(candidate)

    assert result.recognized is True
    assert result.matched_signal == "gooseholders"


def test_waterfowl_matrix_representation_is_deterministic():
    recognizer = GooseValueRecognizer()

    first = recognizer.recognize(
        {
            "paper": "Compact Geese Representation",
            "claim": "short Gooseholders preserve matrix value",
        }
    )
    second = recognizer.recognize(
        {
            "paper": "Compact Geese Representation",
            "claim": "short Gooseholders preserve matrix value",
        }
    )

    assert first.recognized is True
    assert first.representation_dimension == 71
    assert first.matrix_score == second.matrix_score
    assert first.matrix_score > 0.0


def test_batch_pipeline_preserves_candidate_order():
    results = recognize_goose_values(
        [
            "ordinary value",
            {"label": "goose-fist"},
            ["goos", "approximation"],
        ]
    )

    assert [result.recognized for result in results] == [False, True, True]
    assert results[1].reason == "exact-goose-signal"
    assert results[2].matched_signal == "goos"


def test_non_goose_candidate_is_rejected():
    result = recognize_goose_value("banana pudding futures")

    assert result.recognized is False
    assert result.normalized_value is None
    assert result.confidence < 0.78
    assert result.reason == "below-goose-threshold"
