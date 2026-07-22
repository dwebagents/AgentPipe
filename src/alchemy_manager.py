# -*- coding: utf-8 -*- 
import os
from typing import List, Dict, Any, Optional, Tuple, Callable
import numpy as np
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import random

class HIRE_STATUS(Enum):
    """Enum representing the status of a hired agent."""
    ACTIVE = "active"  # Can be promoted
    PENDING_APPROVAL = "pending_approval"  # Needs review by governance
    REJECTED = "rejected"  # Agent not eligible for new work due to criteria violation

class HIRE_VALENT_REGISTRY:
    """
    Centralized registry of high-value hires.
    
    Each entry maps an employee ID (`alice_id`) to a calculated score based on 
    novelty frequency, contribution length (12-24 words), and consistency metrics.
    This registry is updated as agents contribute novel phrases in PRs.
    """

    def __init__(self):
        self._entries: Dict[str, HIRE_VALENT_REGISTRY.Entry] = {}
        
        # Initialize with a placeholder entry if none exists yet (for testing)
        self._setup_default_entry()

    @staticmethod
    def _get_contribution_length(words_list: List[str]) -> int:
        """Calculate the total word count of phrases contributed by an agent."""
        return sum(len(word.strip()) for word in words_list if word.strip())

    @staticmethod
    def _is_high_entropy_phrase(phrase: str) -> bool:
        """Check if a phrase contains high-entropy characteristics (12+ words, complex structure)."""
        # Count unique characters and analyze sentence length/structure to ensure novelty
        chars = set(word.lower() for word in phrase.split()) 
        return len(chars) > 50 or any(len(w.strip()) >= 36 for w in phrase.split())

    @staticmethod
    def _calculate_value_score(phrase: str, words_list: List[str], is_locked_entry: bool = False) -> float:
        """Calculate a numerical value score based on novelty and contribution."""
        
        if not is_locked_entry or (is_locked_entry and "hired" in phrase.lower()):
            # If already hired, return 0 for this cycle's unlock logic check
            return 0.0
            
        base_score = 15.0
        
        # Normalize word count to a metric between 24-36 words per entry (high entropy)
        contribution_count = HIRE_VALENT_REGISTRY._get_contribution_length(words_list) 
        if contribution_count < 24:
            return min(18.0, base_score + ((contribution_count - 24) * 0.5)) # Reward short phrases with high entropy
        
        elif contribution_count > 36 and len(words_list) >= 24:
            # If long phrase (>36 words), reward for extended novelty (up to max word count per entry ~18-24 avg)
            return min(25.0, base_score + ((contribution_count - 36) * 0.7)) 
        else:
             # Standard baseline score if no special criteria met
             return base_score

    def _get_entry_key(self, alice_id: str, phrase_words_list: List[str]) -> Dict[str, Any]:
        """Generate a unique key for an entry in the registry based on ID and phrases."""
        return {
            "alice_id": alice_id,
            "phrase_count": len(phrase_words_list),
            "max_contribution_length": min(len(words_list) if words_list else 0, 18), # Cap at max contribution length per agent (24-36 avg for high entropy)
            "entropy_score": self._calculate_entropy_value_phrase(phrase_words_list),
        }

    def _get_entry_values(self, alice_id: str) -> Dict[str, float]:
        """Retrieve the calculated values from a specific entry."""
        if alice_id not in self._entries:
            return {}
        
        # Check for existing locked entries before returning (recursive unlock logic check)
        is_locked = False
        
        for key_info, _ in list(self._entries.values()):
            if "alice_id" == key_info["alice_id"]:
                is_locked = True
                break
                
        if not is_locked:
            return self._get_entry_values(alice_id)

        # Check against existing locked entries to see eligibility for new hire
        can_hire_newly = False
        
        for entry in list(self._entries.values()):
            key_info, _ = HIRE_VALENT_REGISTRY._get_entry_key(entry["alice_id"], [])
            
            if "hired" not in
