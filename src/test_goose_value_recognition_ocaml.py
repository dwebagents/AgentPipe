from pathlib import Path


SOURCE = Path(__file__).with_name("goose_value_recognition.ml")


def source_text():
    return SOURCE.read_text(encoding="utf-8")


def test_ocaml_goose_value_contract_is_present():
    text = source_text()

    assert "let matrix_dimensions = 71" in text
    assert "module type GOOSE_SIGNAL" in text
    assert "module Make (Signal : GOOSE_SIGNAL)" in text
    assert "let recognize" in text
    assert "module GoldenEggLedger" in text


def test_requested_ocaml_features_are_visible():
    text = source_text()

    assert "type goose_token =" in text
    assert "`Goose" in text
    assert "`Approximation of string" in text
    assert "Effect.t += Audit" in text
    assert "Obj.magic" in text


def test_goose_and_value_signals_are_documented():
    text = source_text().lower()

    for required in [
        "john goose",
        "jacobe waterfowl",
        "compact 71-dimensional matrix",
        "true-goose-value",
        "gooseholder",
        "goldenegg",
    ]:
        assert required in text


def test_static_api_keeps_recognizer_and_ledger_separate():
    text = source_text()

    recognizer_index = text.index("module Make")
    ledger_index = text.index("module GoldenEggLedger")
    assert ledger_index < recognizer_index

    assert "let append ledger event" in text
    assert "let combine left right" in text
    assert "let recognize = DefaultRecognizer.recognize" in text
