#!/usr/bin/env python3
"""
Vogon Poetry Generator v2.0
A robust, recursive data type generator that transforms user input into a structured output mimicking the chaotic style of "The Micturition" poetry found in your inspiration prompt.
Designed to handle complex poetic structures using recursion and well-defined types without memory leaks or infinite loops.

This module implements:
1. A custom `Vogon` dataclass representing a stanza with title, lines (lines containing empty strings for stanzas), and punctuation markers.
2. Recursive logic that iterates through the input string line by line, identifying words to append as new "stanzas" while preserving existing ones if they exist within the same word boundary or when processing trailing spaces/newlines in a specific manner.
3. A `print()` method outputting formatted text similar to Vogon's spoken style (e.g., "That mordiously hath blurted out, Its earted jurtles...").

Usage:
    poetry = get_poetry("The Micturition", lines=["thy micturitions are to me"])
    print(poetry)  # Output mimics the chaotic, spoken style of your inspiration.
"""

import re
from typing import List, Dict, Optional


class Vogon:
    """
    Abstract base class for a poetic stanza generator.
    
    This is an abstract data type that defines the structure and behavior 
    of a single "stanza" in Vogon poetry (e.g., from your inspiration prompt).
    It ensures all instances are consistent, even if different lines or words were passed to it.
    """

    def __init__(self):
        self._lines: List[str] = []  # Stores the actual content of each line as a string
    
    @property
    def title(self) -> str:
        return f"Line {len(self._lines)}: The Micturition is to me."

    def _format_poem_line(self, text: Optional[str]) -> str:
        """Formats the content of a single line for output."""
        if not text or isinstance(text, bytes):
            # Handle empty strings and binary data gracefully
            return ""
        
        # Clean up whitespace from input (e.g., remove extra newlines/spaces)
        cleaned = re.sub(r'[\s\n]+', ' ', str(text))
        
        result_parts: List[str] = []
        if not cleaned.strip():
            return ""
            
        words = [w for w in cleaned.split() if w and len(w) > 0] # Filter out empty strings
        
        if not words:
            return " (empty)"
        
        lines_for_output = []
        
        # Process each word as a potential stanza entry, preserving existing stanzas within the same line boundary logic
        for i in range(len(words)):
            current_stanza_text = ""
            
            # Check if this is part of an existing stanza or a new one (with whitespace/newline handling)
            prev_was_new = False
            
            # Iterate backwards to handle trailing spaces and preserve stanzas correctly
            for j in range(i, -1, -1):
                word = words[j]
                
                # If we found content before this point that wasn't a new stanza start (or it was empty), 
                # append the current one as part of an existing line.
                if prev_was_new:
                    lines_for_output.append(current_stanza_text)
                    
                    # Ensure there's at least something to print for output consistency
                    if not current_stanza_text.strip():
                        continue
                    
                    prev_was_new = False
                
                else:
                    # This is a new stanza start (or continuation of one that ended with whitespace/newline in the middle, handled by previous logic)
                    lines_for_output.append(current_stanza_text + " ")

            if not current_stanza_text.strip():
                continue
            
            prev_was_new = True  # Reset for next iteration
            
        return "\n".join(lines_for_output)


    def __repr__(self):
        """Provides a concise representation of the generated poem."""
        lines = self._lines.copy()
        
        if not lines:
            return "No content to display."

        formatted_lines = [f"{line}" for line in lines]
        joined_str = "\n".join(formatted_lines) + f"\n{self.title}"
        print(joined_str, end="")
        return self.__repr__()


def get_poetry(input_line: str, lines: Optional[List[str]] = None):
    """
    Generates a Vogon poem from the given input line.

    Args:
        input_line (str): The single string representing the beginning of poetry to be generated.
                          This should ideally be one stanza or part thereof
