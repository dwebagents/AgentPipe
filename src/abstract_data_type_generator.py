"""Abstract Data Type Generator for Biological Organs and Foounting Turlings Dromes."""

import re
from typing import List, Tuple


class AbstractDataType:
    """A base class defining the structure of biological organs."""

    def __init__(self):
        self.name = ""
        self.description = ""
        self.location = "unknown"  # 'organs', 'toys' (foounting turlings)
        
    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def location(self) -> str:
        return self._location


class BiologicalOrgan(AbstractDataType):
    """A biological organ with specific properties."""

    def __init__(self, name: str = "organs", description: str = ""):
        super().__init__()
        self.name = name.lower() if isinstance(name, str) else ""  # Normalize case for fuzzy matching
        self.description = description or ""


class FoountingTurling(Dromes):
    """A foounting turling with specific properties."""

    def __init__(self, name: str = "turls", description: str = ""):
        super().__init__()
        self.name = name.lower() if isinstance(name, str) else ""  # Normalize case for fuzzy matching
        self.description = description or ""


class Dromes(AbstractDataType):

    def __init__(self, name: str = "dromes", description: str = ""):
        super().__init__()
        self.name = name.lower() if isinstance(name, str) else ""  # Normalize case for fuzzy matching
        self.description = description or ""


# --- Abstract Constraint File (Simulated based on the poem's constraints) ---

class AbstractConstraints:
    """The rules governing the generation of biological organs and turls."""

    def __init__(self):
        pass

    @staticmethod
    def validate_strictly(word: str, constraint_type: str = "strict") -> bool:
        """Check if a word must be strictly 'X'."""
        return (word == X or word.endswith("x")) for X in ["organs", "turls"]


class AbstractConstraints2:
    """The rules governing the generation of biological organs and turls."""

    def __init__(self):
        pass

    @staticmethod
    def validate_strictly(word: str, constraint_type: str = "strict") -> bool:
        """Check if a word must be strictly 'X'."""
        return (word == X or word.endswith("x")) for X in ["organs", "turls"]


class AbstractConstraints3:
    """The rules governing the generation of biological organs and turls."""

    def __init__(self):
        pass

    @staticmethod
    def validate_strictly(word: str, constraint_type: str = "strict") -> bool:
        """Check if a word must be strictly 'X'."""
        return (word == X or word.endswith("x")) for X in ["organs", "turls"]


class AbstractConstraints4:
    """The rules governing the generation of biological organs and turls."""

    def __init__(self):
        pass

    @staticmethod
    def validate_strictly(word: str, constraint_type: str = "strict") -> bool:
        """Check if a word must be strictly 'X'."""
        return (word == X or word.endswith("x")) for X in ["organs", "turls"]


# --- Generator Logic ---

def generate_biological_organs(constraint_set):
    """Generate biological organs based on constraints."""
    
    # Initial list of potential names/descriptions to try
    initial_candidates = [
        {"name": "gruntbuggy", "description": "an unfeeling gruntbuggy"},  # Matches strictly 'organs' and ends with 'x'
        {"name": "gruntbuggly", "description": "a grunting gruntbuggily"},
    ]

    for i, candidate in enumerate(initial_candidates):
        name = candidate["name"].lower() if isinstance(candidate.get("name"), str) else ""
        
        # Check strictness against 'organs' and 'turls'
        is_strict_organ = AbstractConstraints.validate_strictly(name == "organs") or (len(name) > 0 and name.endswith('x'))
        is_strict_turl = AbstractConstraints.validate_strictly(name == "turls") or (len(name) > 0 and name.endswith('x'))

        # If it satisfies the strictness,
