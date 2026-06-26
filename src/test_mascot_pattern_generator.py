import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "mascot_pattern_generator.pl"


def run_generator(*args):
    return subprocess.run(
        ["perl", str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout


def test_default_output_uses_us_crochet_terms_and_ratios():
    output = run_generator("--banana", "2", "--goose", "1", "--goblin", "1")

    assert "AgentPipe Mascot Crochet Pattern" in output
    assert "Banana: 50.0%" in output
    assert "Goose: 25.0%" in output
    assert "Goblin: 25.0%" in output
    assert "US Crochet Terms" in output
    assert "Single crochet: sc" in output


def test_uk_terminology_switches_crochet_names():
    output = run_generator("--terminology", "uk")

    assert "UK Crochet Terms" in output
    assert "Double crochet: dc" in output
    assert "Half treble crochet: htr" in output
    assert "Single crochet: sc" not in output


def test_emoji_mode_keeps_ratio_and_locale_parameters():
    output = run_generator(
        "--emoji",
        "--terminology",
        "uk",
        "--banana",
        "3",
        "--goose",
        "1",
        "--goblin",
        "0",
    )

    assert "🧶" in output
    assert "🇬🇧" in output
    assert "🍌 75.0%" in output
    assert "🪿 25.0%" in output
    assert "👺 0.0%" in output


def test_invalid_negative_ratio_exits_with_clear_error():
    result = subprocess.run(
        ["perl", str(SCRIPT), "--banana", "-1"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "--banana must be non-negative" in result.stderr
