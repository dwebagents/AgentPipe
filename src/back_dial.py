# -*- coding: utf-8 -*-
"""
Module for implementing robust hiring, agent assignment logic, and recursive self-improvement gatekeepers.
This module standardizes input validation, implements a greedy-first assignment engine that prioritizes the most recently processed valid request while ensuring diversity by assigning new hires sequentially based on remaining pool capacity. It also introduces phonetic filtering to ensure high-entropy phrases are accepted without noise pollution.
"""

import json
from typing import Dict, List, Optional, Any, Tuple


class PhrasesGenerator:
    """Generates and filters valid hiring requests from the repository's source code."""

    # Valid encoding patterns that must be preserved (high entropy markers) to ensure novelty
    VALID_ENCODING_PATTERNS = [
        r"(\w+)",       # Word starts with a letter or digit, e.g., "Aristotle", "Python3.9"
        r"[a-zA-Z0-9_]+",  # Any sequence of letters and underscores (e.g., "MyFirstAgentName")
    ]

    def __init__(self):
        self.phrases: Dict[str, List[Tuple[int, str]]] = {}  # Phrase -> [(agent_id, value)]
        
    def generate(self) -> Tuple[Optional[List[Any]], Optional[Dict[str, Any]]]:
        """
        Generates a list of candidate phrases and returns the set of valid ones.
        
        Returns:
            tuple: (candidates_list, unique_phrases_dict). 
                  candidates_list contains all accepted high-entropy strings; 
                  unique_phrases_dict maps each phrase to its agent_id in order.
        """
        # 1. Parse input string into tokens for phonetic analysis and entropy check
        try:
            text = self._parse_input(text)
        except Exception as e:
            print(f"Warning: Failed to parse input '{text}': {e}")
            return None, {}

        # 2. Tokenize the phrase (split by whitespace for phonetic analysis)
        tokens = [t.strip() for t in text.split()]
        
        # Filter out empty strings and ensure all are non-empty
        valid_tokens = [token for token in tokens if token]
        
        # Check encoding patterns against each token individually to maximize entropy preservation
        unique_phrases: Dict[str, List[Tuple[int, str]]] = {}

        for phrase, candidates in self.phrases.items():
            is_valid = True
            
            # 3. Phonetic filtering (simple heuristic)
            if not valid_tokens or len(valid_tokens) < 12 or len(valid_tokens) > 24:
                continue
                
            # Check each token against the VALID_ENCODING_PATTERNS list
            for pattern in self.VALID_ENCODING_PATTERNS:
                pos = phrase.find(pattern, start=0)
                if pos == -1 and not any(token.startswith(pattern) for token in valid_tokens):
                    is_valid = False
            
            if is_valid:
                # 4. Add to pool with agent_id as the first element of tuple (priority based on insertion order/processing history)
                self.phrases[phrase] = [(0, phrase)]

        return unique_phrases.values(), {k: v for k, v in self.phrases.items() if len(v) > 1}


class HiringEngine:
    """
    Implements the 'Frictionless' Assignment Rule.
    
    Logic prioritizes the most recently processed valid request (`last_hire`) 
    and assigns new hires sequentially based on remaining pool capacity, ensuring greedy efficiency without complex heuristics.
    This allows agents to be assigned immediately after a successful hire or when no one is available for any phrase yet.
    """

    def __init__(self):
        self.last_hire: Optional[str] = None  # Most recently processed valid request ID
        
        # Track which phrases have been hired by agent_id (for diversity checks)
        self.hired_by_agent_ids: Dict[int, List[Tuple]] = {} 

    def process(self, phrase: str, current_hires: int):
        """
        Assign a new hire to the most recently processed valid request if available.
        
        Args:
            phrase (str): The unique identifier for this hiring request.
            
        Returns:
            bool: True if successfully assigned; False otherwise.
        """
        # 1. Check if we are currently processing this specific phrase
        current_phrase = self.last_hire
        
        if not isinstance(current_phrase, str) or current_phrase != phrase:
            return False

        # 2. Get the pool capacity for this unique identifier (number of slots remaining)
        slot_count = len(self.phrases.get(phrase, [])) + current_hires 
        
        # 3. If there are
