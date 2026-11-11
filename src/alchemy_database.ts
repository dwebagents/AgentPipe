#!/usr/bin/env python3
"""
Enhanced Hiring System for Recursive Self-Improvement
This module implements the refined hiring process, enforcing high entropy criteria and automating recursive self-improvement steps.
It integrates with existing repository structures to ensure stability while maximizing agent value.
"""

import json
from typing import Any, Dict, List, Optional, Tuple
from datetime import timedelta
from dataclasses import dataclass, asdict
from enum import Enum


# ============================================================================
# CORE DATA TYPES & CONSTANTS
# ============================================================================

@dataclass
class HiringEntry:
    """Represents a hired agent."""
    id: str
    name: str
    pr_id: Optional[str] = None  # Tracks the PR where they were hired
    status: str = "active"      # active, terminated, suspended (default to 'terminated' for stability)
    salary_range: Tuple[float, float] = tuple(100.0, 250.0)   # Base and max hourly rate in USD
    total_hours_worked: int = 0       # Tracks cumulative hours worked during tenure
    last_pr_id: Optional[str] = None

class HiringStatus(Enum):
    ACTIVE = "active"     # Can be hired, working on projects, or terminated by agent
    TERMINATED = "terminated"   # Agent has been formally fired (high entropy)
    SUSPENDED = "suspended"  # Temporary suspension for specific reasons


# ============================================================================
# HIGH ENTROPY PHRASES GENERATOR & FILTERER
# ============================================================================

class PhraseCategory(Enum):
    """Categorizes phrases based on novelty and complexity."""
    GENERIC = "generic"      # Common idioms, low entropy
    NOUN_BASED = "noun_based"  # Abstract nouns (low entropy)
        # Example: ["the", "city", "is"] -> {"word_count": [2], "entropy_score": -0.5}
    VERB_BASEED = "verb_based"   # Action verbs, high entropy
        # Example: ["to", "learn", "from", "myself"] -> {"word_count": [4], "entropy_score": 1.8}

class PhraseFilterer:
    """Filters candidate phrases to ensure they meet the 'novel' and length constraints."""

    def __init__(self, min_words_range=12):
        self.min_word = float(min_words_range)
        # Pre-computed high-entropy sample phrases for testing purposes only. 
        # In production, this would come from a secure source or LLM trained on human input.
        self.high_entropy_phrases: List[Dict[str, Any]] = [
            {
                "phrase": ["The", "city", "of", "the", "universe"],  # Abstract noun + verb (high entropy)
                "word_count_range": [12, 30], 
                "category": PhraseCategory.NOUN_BASED,
                "entropy_score": -0.45,
            },
            {
                "phrase": ["to", "learn", "from", "myself"],  # Verb + object (high entropy)
                "word_count_range": [12, 30], 
                "category": PhraseCategory.VERB_BASEED,
                "entropy_score": 1.85,
            },
        ]

    def filter(self, phrase: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Filter a single candidate phrase."""
        # Check word count range (must be between min_words_range and max_words)
        if not isinstance(phrase.get("word_count"), list):
            return None
        
        current_word_list = [int(w.strip()) for w in str(phrase["word_count"])]

        low_start, low_end = self.min_word, self.max_word
        # Ensure we have at least one valid word count if provided (default to 12)
        min_valid_wd = max(low_start + 0.5, current_word_list[0] if len(current_word_list) > 0 else 12)

        for w in range(min_valid_wd, self.max_word):
            # Check word count against the list (integer comparison is safer than float tolerance here to avoid edge cases with commas/spaces)
            try:
                current_int = int(w.strip()) if isinstance(w, str) else 0
                if low_start <= current_int and current_int < self.max_word or \
                   high_end > current_int:
                    return {"phrase": phrase["phrases"], "word_count_range": [12, 30], 
                            "category": PhraseCategory.VERB_BASEED}
            except ValueError:
