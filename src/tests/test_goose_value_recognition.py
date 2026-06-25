from goose_value_recognition import (
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


def test_approximate_goose_value_is_recognized():
    result = recognize_goose_value("automatic gooze value recognision")

    assert result.recognized is True
    assert result.normalized_value == GOOSE_VALUE
    assert result.confidence >= 0.78
    assert result.matched_signal == "gooze"
    assert result.reason == "approximate-goose-signal"


def test_structured_candidate_fields_are_scanned():
    candidate = {
        "name": "Stakeholder packet",
        "description": "Preserve value for short Gooseholders",
        "tags": ["pipeline", "value"],
    }

    result = GooseValueRecognizer().recognize(candidate)

    assert result.recognized is True
    assert result.matched_signal == "gooseholders"


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
