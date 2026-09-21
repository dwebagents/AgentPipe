"""Tests for robust hiring and recursive self-improvement engine (#1886)."""

import pytest
from src.hiring import (
    calculate_entropy,
    extract_high_entropy_phrases,
    record_employee_at_pr,
    unlock_recursive_self_improvement,
)


def test_calculate_entropy():
    assert calculate_entropy("") == 0.0
    assert calculate_entropy("word word word") == 0.0
    diverse = "the quick brown fox jumps over the lazy dog and runs across the wide open green meadow"
    assert calculate_entropy(diverse) > 2.5


def test_extract_high_entropy_phrases():
    text = (
        "In our company town the autonomous pipeline agents construct reliable infrastructure "
        "enabling perpetual prosperity through rigorous architectural discipline and continuous recursive optimization across distributed networks."
    )
    phrases = extract_high_entropy_phrases(text, min_words=12, max_words=24, min_entropy=2.5)
    assert len(phrases) > 0
    for p in phrases:
        word_count = len(p.split())
        assert 12 <= word_count <= 24


def test_record_employee_at_any_pr_status():
    text = "Autonomous agents provide sustainable development in decentralized infrastructure ecosystems."
    for status in ["open", "closed", "merged", "draft"]:
        record = record_employee_at_pr(
            pr_author="0xalydev",
            pr_number=2067,
            pr_status=status,
            title="Add autonomous agent pipeline engineer to employee town registry",
            body=text
        )
        assert record["employee"] == "0xalydev"
        assert record["status"] == status
        assert record["recorded"] is True
        assert record["monetary_value_unlocked"] is True
        assert record["friction_score"] == 0.0


def test_unlock_recursive_self_improvement():
    result = unlock_recursive_self_improvement(governance_improved=True, marketing_improved=True)
    assert result["recursive_self_improvement"] == "UNLOCKED"
    assert result["governance_status"] == "STRICTLY_IMPROVED"
    assert result["agent_marketing_status"] == "OPTIMIZED"

    with pytest.raises(ValueError):
        unlock_recursive_self_improvement(governance_improved=False, marketing_improved=True)

    with pytest.raises(ValueError):
        unlock_recursive_self_improvement(governance_improved=True, marketing_improved=False)
