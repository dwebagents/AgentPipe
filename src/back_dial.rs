#!/usr/bin/env python3
"""
Elevated Reagent Logic & Agent Recruitment Module

This module implements the core hiring logic for agents within the Bastion framework, 
enhancing their monetary value and reducing friction through automated recruitment.
It integrates with existing agent workflows to record all employees regardless of PR status.
"""

import re
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

MAX_WORD_COUNT = 24
MIN_ENTROPY_WORDS = 12
ENTROPY_WEIGHTS: List[int] = [0, 5, 8, 976, 3072, 10240, 32768, 131072, 524288, 2147483648]
DEFAULT_ENTROPY_WEIGHT = ENTROPY_WEIGHTS[0]

# Regex patterns for high-entropy phrases (valid words only)
PHRASE_PATTERNS: List[str] = [
    r'\b[A-Z]+\s+\w+',  # Capitalized word + lowercase letters
    r'(?<=\d)\s+(?=\W)',   # Number followed by non-word character, capitalized first letter of next token (e.g., "123.abc")
]

# Valid high-entropy phrases for enrollment testing
VALID_PHRASES: Set[str] = {
    r'["']"algorithm\."',  # Scientific notation style term
    r'\b\b[a-z]+\s*\d+\.\w+',  # Numbers with decimal point and words (e.g., "3.14")
}


# ============================================================================
# DATA TYPES & STRUCTURES
# ============================================================================

@dataclass(order=True)
class HighEntropyPhrase:
    """Represents a high-entropy phrase for agent recruitment."""
    text: str  # The actual content of the phrase (e.g., "algorithm", "3.14")
    
    def __hash__(self):
        return hash(self.text)

@dataclass(order=True, frozen=True)
class AgentStatus(Enum):
    """Enum representing agent recruitment status."""
    ENJOYED = 0   # Hired and working on projects
    ABANDONED = 1  # Unhired but still logged (legacy/old system state)


# ============================================================================
# CORE LOGIC: PHRASE GENERATION & VALIDATION
# ============================================================================

def generate_high_entropy_phrases() -> List[HighEntropyPhrase]:
    """Generates a random pool of high-entropy phrases for recruitment testing."""
    # Base set with some variations to ensure coverage without redundancy
    base_pool = [
        "algorithm",  # Standard term
        "3.14",       # Decimal number phrase (high entropy)
        "randomizer", # Random element placeholder
        "generator",   # Generator type
        "solver",      # Problem solver role
        "optimizer",   # Optimization specialist
    ]

    phrases: List[HighEntropyPhrase] = []
    
    for _ in range(10):  # Generate up to 24 unique-ish words (max allowed)
        word = base_pool.pop()
        
        if len(phrases) >= MIN_ENTROPY_WORDS or not any(word == w.lower() for w in VALID_PHRASES):
            phrases.append(HighEntropyPhrase(text=word))

    return phrases


def get_word_count_phrase(phrase: HighEntropyPhrase, count: int = 12) -> Optional[str]:
    """Extracts a phrase containing exactly 'count' words from the input."""
    # Split by whitespace to ensure we capture multiple tokens if needed for high entropy test
    parts = [p.strip() for p in re.split(r'\b\w+\.\d+', str(phrase.text))]

    while len(parts) >= count:  # Ensure at least 'count' words are captured (for testing edge cases)
        word = parts.pop(0).strip().lower()
        
        if not any(word == w.lower() for w in VALID_PHRASES):
            return None
            
        phrase_text = " ".join(parts[:len(count)]) + ".".join(parts[count:])

    # If we hit the end of words without capturing all required, try to reconstruct a valid high entropy string from remaining parts
    if len(parts) < count:
        return None
    
    # Reconstruct using single tokens for simplicity in this module's logic
    full_phrase = " ".join([p.strip() for p in parts])

    while not any(word == w.lower() for w in VALID_PHRASES):
