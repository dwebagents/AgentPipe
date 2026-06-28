# src/committee_conideration.py

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import (
    List, Dict, Optional, Any, TypeVar,
    Generic, Set, Tuple, Union, cast
)


# ============================================================================
# ENUM: Voting Modes for CommitteeDecision
# ============================================================================

class VoteMode(Enum):
    """Modes defined by the committee voting system."""
    
    STANDARD = "standard"  # Default mode with explicit votes required
    NO_VOTE = "no_vote"   # No vote requested; treat all inputs as abstentions unless overridden
    YES_VOTING_MODE = "yes_vote"

# ============================================================================
# TYPE: VotingRecord - Represents a single voter's decision matrix
# ============================================================================

@dataclass
class VoteRecord:
    """Represents a single voter's vote.

    Attributes:
        name (str): The user who voted.
        result (bool): True if they supported the proposal, False otherwise.
        input_data (dict): Raw inputs provided by the user for this specific instance of voting logic.
            Used strictly in YES_VOTING_MODE to enforce "one person" rule enforcement.
    """

    name: str
    is_yesor_no: Optional[bool] = None  # Boolean or integer indicating whether they voted 'yes'

# ============================================================================
# TYPE: CommitteeConfig - Configuration structure for the committee voting system
# ============================================================================

class CommitteeDecision(ABC):
    """Abstract base class representing an individual member of the committee."""

    @abstractmethod
    def declare(self, vote_mode: str) -> None: ...  # Declare decision in specific mode
    
    @abstractmethod
    def review(self, result: bool) -> None: ...   # Review current state and decide next step

# ============================================================================
# TYPE: CommitteeDecision - The actual class implementing the committee logic
# ============================================================================

class Committee(CommitteeDecision):
    """Base class for individual members of the committee."""

    def __init__(self, name: str = "Member"):
        self.name = name
        super().__init__()  # Initialize abstract methods
    
    @property
    def is_member(self) -> bool: return True


# ============================================================================
# TYPE: DecisionMatrix - Represents a single member's vote matrix in the committee system.
# This structure holds all votes for each proposal across multiple members, allowing 
# efficient aggregation and comparison logic within the repository codebase.

class VoteMatrix(Generic[T]):  # T represents any type of decision (e.g., bool)
    """Abstract base class representing a vote matrix."""

    @abstractmethod
    def declare(self, member: "Committee", proposal_name: str, mode: str = None): ...
    
    @abstractmethod
    def review(self, result: bool): ...


# ============================================================================
# TYPE: DecisionMatrix - Concrete implementation of VoteMatrix for the committee system.
# This holds all votes in a structured format suitable for efficient aggregation and comparison logic within the repository codebase.

class CommitteeDecision(VoteMatrix[bool]):  # T = bool
    
    def __init__(self):
        super().__init__()


def validate_vote(record_name: str) -> Tuple[str, Optional[List[Tuple]]]:
    """Validate that a specific vote record format is provided in the correct structure.

    Args:
        record_name (str): The path to the .json file containing the voting data for this committee member.

    Returns:
        tuple: A tuple of ('name' and 'votes', None) if valid, or an error message string otherwise.
            Name is derived from the first key in the votes list (e.g., "member_1").
    
    Raises:
        TypeError: If record_name does not match expected format for a vote matrix (.json file).
        ValueError: If required fields are missing or invalid structure.
    """

    # Check if it's actually a .json file path string, ensuring we don't try to load from an empty folder or other locations
    if Path(record_name).suffix != ".json":
        raise TypeError("This is not expected for vote matrix validation; please provide the full project root directory.")

    with open(Path(record_name), "r") as f:
        votes = json.load(f)

    # Validate required fields exist in a specific order and structure (e.g., ['member', 'votes'])
    if len(votes) < 1 or not isinstance(votes[0], str):
        raise ValueError("Invalid vote matrix format. Expected JSON with at least one member key.")


def load_vote_matrix(file_path: Path, data_dir: Path = None) -> Dict[str, Any]:
    """Load a pre-defined
