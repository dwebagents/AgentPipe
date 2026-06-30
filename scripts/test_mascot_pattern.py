import subprocess
import re
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "agentpipe_mascot.pl"

# Locate perl on Windows (common Git-for-Windows path) or use PATH
_PERL = "perl"
for _candidate in (
    r"C:\Program Files\Git\usr\bin\perl.exe",
    os.path.expandvars(r"%ProgramFiles%\Git\usr\bin\perl.exe"),
):
    if os.path.exists(_candidate):
        _PERL = _candidate
        break


def _perl_args(*args):
    return [_PERL, str(SCRIPT), *args]


def run(*args):
    return subprocess.run(
        _perl_args(*args),
        cwd=ROOT,
        text=True,
        encoding='utf-8',
        capture_output=True,
        check=True,
    ).stdout


def run_no_check(*args):
    return subprocess.run(
        _perl_args(*args),
        cwd=ROOT,
        text=True,
        encoding='utf-8',
        capture_output=True,
    )


# ---------------------------------------------------------------------------
# Syntax check
# ---------------------------------------------------------------------------

def test_perl_syntax():
    result = subprocess.run(
        [_PERL, "-c", str(SCRIPT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert "syntax OK" in result.stderr or "syntax OK" in result.stdout


# ---------------------------------------------------------------------------
# Basic output
# ---------------------------------------------------------------------------

def test_default_output_includes_overview():
    output = run("--banana", "2", "--goose", "1", "--goblin", "1")
    assert "# AgentPipe Mascot" in output
    assert "## Overview" in output
    assert "50%" in output
    assert "25%" in output


def test_default_uses_us_terminology():
    output = run()
    assert "stockinette / sc" in output


def test_custom_name_appears():
    output = run("--name", "Test Mascot")
    assert "# Test Mascot" in output


# ---------------------------------------------------------------------------
# UK terminology
# ---------------------------------------------------------------------------

def test_uk_terminology_converts_sc_to_dc():
    output = run("--terminology", "uk")
    assert "stockinette / dc" in output
    assert "Magic ring, 6 dc" in output


def test_uk_terminology_converts_sc2tog_to_dc2tog():
    output = run("--terminology", "uk")
    assert "dc2tog" in output


def test_uk_terminology_does_not_chain():
    output = run("--terminology", "uk")
    matches = re.findall(r"stockinette / \w+", output)
    for m in matches:
        assert "dtr" not in m, f"Chaining detected: {m}"
        assert "tr" not in m, f"Over-chaining detected: {m}"


# ---------------------------------------------------------------------------
# Emoji mode
# ---------------------------------------------------------------------------

def test_emoji_output_contains_crochet_hook():
    output = run("--emoji", "--craft", "crochet")
    assert "\U0001FA9D" in output  # 🪝


def test_emoji_output_contains_knit_yarn():
    output = run("--emoji", "--craft", "knit")
    assert "\U0001F9F6" in output  # 🧶


def test_emoji_and_uk_terminology_combine():
    output = run("--emoji", "--terminology", "uk")
    assert "\U0001FA9D" in output or "\U0001F9F6" in output


# ---------------------------------------------------------------------------
# Output formats
# ---------------------------------------------------------------------------

def test_html_output_has_doctype():
    output = run("--format", "html")
    assert "<!DOCTYPE html>" in output


def test_html_output_has_closing_tags():
    output = run("--format", "html")
    assert "</html>" in output


def test_text_output_no_markdown_headers():
    output = run("--format", "text")
    assert "# AgentPipe Mascot" not in output
    assert "Overview" in output


# ---------------------------------------------------------------------------
# Crafts
# ---------------------------------------------------------------------------

def test_crochet_output_has_magic_ring():
    output = run("--craft", "crochet")
    assert "Magic ring" in output


def test_knit_output_has_cast_on():
    output = run("--craft", "knit")
    assert "Cast on" in output


# ---------------------------------------------------------------------------
# Ratios
# ---------------------------------------------------------------------------

def test_pure_banana():
    output = run("--banana", "1", "--goose", "0", "--goblin", "0")
    assert "100%" in output


def test_pure_goose():
    output = run("--banana", "0", "--goose", "1", "--goblin", "0")
    assert "100%" in output


def test_pure_goblin():
    output = run("--banana", "0", "--goose", "0", "--goblin", "1")
    assert "100%" in output


def test_uneven_ratios():
    output = run("--banana", "5", "--goose", "3", "--goblin", "2")
    assert "50%" in output
    assert "30%" in output
    assert "20%" in output


# ---------------------------------------------------------------------------
# Scaling
# ---------------------------------------------------------------------------

def test_scale_affects_height():
    small = run("--scale", "0.5")
    large = run("--scale", "2.0")
    small_height = re.search(r"Height.*?(\d+\.?\d*)", small)
    large_height = re.search(r"Height.*?(\d+\.?\d*)", large)
    assert small_height and large_height
    assert float(small_height.group(1)) < float(large_height.group(1))


# ---------------------------------------------------------------------------
# Yarn weights
# ---------------------------------------------------------------------------

def test_all_yarn_weights_produce_output():
    for weight in ("lace", "fingering", "sport", "dk", "worsted", "bulky"):
        output = run("--yarn-weight", weight)
        assert f"Yarn weight:** {weight}" in output


# ---------------------------------------------------------------------------
# Progress checkboxes
# ---------------------------------------------------------------------------

def test_output_contains_checkboxes():
    output = run()
    assert "☐" in output


def test_body_complete_checkbox():
    output = run()
    assert "☐ Body complete" in output


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

def test_materials_section():
    output = run()
    assert "Materials" in output
    assert "yarn" in output
    assert "Stuffing" in output
    assert "Eyes" in output
    assert "stitch markers" in output


def test_colour_allocation():
    output = run("--banana", "1", "--goose", "1", "--goblin", "1")
    assert "Motif" in output
    assert "Ratio" in output
    assert "Main colour" in output
    assert "Accent 1" in output
    assert "Accent 2" in output


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def test_assembly_section():
    output = run()
    assert "Assembly" in output
    assert "Body preparation" in output
    assert "Attaching motifs" in output


def test_face_embroidery():
    output = run("--banana", "2", "--goose", "0", "--goblin", "0")
    assert "banana dominant" in output.lower() or "soft curved brows" in output


# ---------------------------------------------------------------------------
# Finishing
# ---------------------------------------------------------------------------

def test_finishing_section():
    output = run()
    assert "Finishing" in output
    assert "Weave in all ends" in output


def test_customisation_section():
    output = run()
    assert "Customisation" in output
    assert "--scale" in output


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_negative_ratio_fails():
    result = run_no_check("--banana", "-1")
    assert result.returncode != 0


def test_unknown_yarn_weight_fails():
    result = run_no_check("--yarn-weight", "cobweb")
    assert result.returncode != 0
    assert "Unknown" in result.stderr


def test_invalid_craft_fails():
    result = run_no_check("--craft", "sewing")
    assert result.returncode != 0
    assert "Craft must be" in result.stderr


def test_zero_total_ratio_fails():
    result = run_no_check("--banana", "0", "--goose", "0", "--goblin", "0")
    assert result.returncode != 0
    assert "At least one ratio" in result.stderr


def test_invalid_format_fails():
    result = run_no_check("--format", "pdf")
    assert result.returncode != 0


# ---------------------------------------------------------------------------
# --help
# ---------------------------------------------------------------------------

def test_help_shows_options():
    result = run_no_check("--help")
    assert result.returncode == 0
    assert "--banana" in result.stdout
    assert "--goose" in result.stdout
    assert "--goblin" in result.stdout
    assert "--terminology" in result.stdout
    assert "--emoji" in result.stdout
    assert "--yarn-weight" in result.stdout
    assert "--craft" in result.stdout
    assert "--scale" in result.stdout
    assert "--format" in result.stdout
