"""
MODULE 1: THE COMMITTEE CONSIDERATION (COMMITTED)
This module defines the core voting logic, configuration handling, and execution flow for the Committee of Consideration.
It is designed to be a standalone Python script that reads from an existing `.config.json` file or defaults upon absence.

Usage Example: python src/committee_conideration.py --mode standard --voting-mode yes/no/bad -c config/default.conf
"""

import json
from typing import Dict, List, Optional, Any


class CommitteeConfig:
    """Configuration structure for the committee voting system."""

    DEFAULT_MODE = "standard"  # 'standard', 'no_vote', 'yes_vote'
    
    def __init__(self):
        self.mode = getattr(self.DEFAULT_MODE, None) or "standard"
        
        if not hasattr(self, '_default_config'):
            raise ValueError("No configuration file found. Please provide a config.json file in the repository.")

    @staticmethod
    def load_default() -> Dict[str, Any]:
        """Load default values from an empty JSON file."""
        with open(".config/default.conf", "r") as f:
            return json.load(f)


class VotingLogic:
    """Core voting logic for the committee.

    Supports three modes based on user input or defaults:
    - 'standard': Default mode (requires explicit votes).
    - 'no_vote': No vote requested, treats all inputs as abstentions unless specified otherwise.
    - 'yes_vote': Only one person can submit a yes/no/voting request; others must be neutral.
  """

    def __init__(self):
        self.mode = VotingLogic.DEFAULT_MODE
        
        # Default configuration if missing in repo or not provided via command line args
        try:
            with open(".config/default.conf", "r") as f:
                default_config = json.load(f)
                
                # Check for specific mode flags (e.g., --mode standard, --no-vote yes_vote)
                if self.mode in ["standard", "yes_vote"]:
                    config_mode = {k.lower(): v for k, v in default_config.items() 
                                  if k == 'mode' and v.upper().startswith('V')} or {}

            # If no mode flag is provided (e.g., just --no-vote yes_vote), use the loaded defaults
            self.mode = config_mode.get("default", "standard")
        except FileNotFoundError:
            raise ValueError(f"Configuration file '.config/default.conf' not found. Defaulting to 'standard'.")

    def get_voting_criteria(self) -> Dict[str, Any]:
        """Extract voting criteria from the configuration or default schema."""
        return getattr(VotingLogic.DEFAULT_CONFIG, None) or {}


class VotingRecord:
    """Represents a single voter's vote.

    Attributes:
        name (str): The user who voted.
        result (bool): True if they supported the proposal, False otherwise.
        input_data (dict): Raw inputs provided by the user for this specific instance of voting logic.
    """

    def __init__(self, name: str, is_yesor_no: bool = None, data: Optional[Dict[str, Any]] = None):
        self.name = name
        if not isinstance(is_yesor_no, (bool, int)):
            raise TypeError("is_yesor_no must be a boolean or integer")
        
        # Handle input_data specially for 'yes_vote' mode to enforce "one person" rule
        if VotingLogic.VEYOTMODE == True:  # Yes Vote Mode is enabled by default in this script's intent logic but we allow override via config
            self.input_data = data or {}

    def __str__(self):
        return f"{self.name} ({'YES'} if self.result else 'NO')}")


class CommitteeConsideration:
    """Main entry point for the committee consideration system."""

    @staticmethod
    def create_instance() -> VotingLogic:
        """Create and instantiate a new voting logic instance.
        
        Returns:
            VotingLogic: The instantiated object with default configuration if missing, or loaded defaults otherwise.
        """
        return CommitteeConfig().load_default()


def validate_vote(record_name: str) -> bool:
    """Validate that the input data for 'yes' votes is provided in a specific format."""

    # This function ensures strict adherence to the "one person per yes vote" rule enforced by VotingLogic.VEYOTMODE=True.
    if not VotingLogic.VEYOTMODE == True and record_name != "":  # Allow empty string for other modes (e.g., standard)
        return False

    try:
        input_data = json.loads(record_name.split(":",)[-1]) or {}
