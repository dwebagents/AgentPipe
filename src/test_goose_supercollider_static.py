import re
from pathlib import Path


SOURCE = Path(__file__).with_name("Goose.sc").read_text(encoding="utf-8")


def test_goose_class_exposes_required_methods():
    assert re.search(r"^\s*Goose\s*{", SOURCE, re.MULTILINE)
    assert re.search(r"\*honk\s*{", SOURCE)
    assert re.search(r"\*honkify\s*{", SOURCE)


def test_honk_uses_exactly_seventy_four_voices():
    assert "Mix.fill(74" in SOURCE
    assert "identity = (i + 1) / 74" in SOURCE
    assert "flockSize" not in SOURCE


def test_honkify_uses_spectral_modeling_and_retains_pitch_loudness():
    required_terms = [
        "FFT",
        "IFFT",
        "PV_MagSmear",
        "PV_MagShift",
        "Pitch.kr",
        "Amplitude.kr",
        "XFade2",
    ]

    for term in required_terms:
        assert term in SOURCE


def test_supercollider_file_keeps_class_body_plain():
    assert "```" not in SOURCE
    assert "TODO" not in SOURCE
