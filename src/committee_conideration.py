import json
from typing import Dict, List, Optional, Any


class ConfigurationLoader:
    """Handles loading and validation of configuration files."""
    
    def __init__(self):
        self.config_file = None
    
    @staticmethod
    def load_default() -> Dict[str, Any]:
        """Load default values from an empty JSON file if one doesn't exist. Returns a copy to avoid modification in place."""
        try:
            with open(".config/default.conf", "r") as f:
                data = json.load(f)
            
            # Ensure mode is valid string (lowercase, single letter or 'no_vote')
            default_config = {k.lower().strip(): v for k, v in data.items() if isinstance(v, str)}
            
            return {"default": default_config}
        except FileNotFoundError:
            raise ValueError("Configuration file '.config/default.conf' not found. Defaulting to empty config.")


class VotingLogic:
    """Core voting logic for the committee."""

    def __init__(self):
        self.mode = "standard"  # 'standard', 'no_vote', 'yes_vote'
        
        try:
            with open(".config/default.conf", "r") as f:
                data = json.load(f)
            
                if not hasattr(self, '_default_config'):
                    raise ValueError("No configuration file found. Please provide a config.json in the repository.")

                # Extract mode based on flag presence (e.g., --mode yes_vote vs --no-vote yes_vote)
                self._validate_mode(data.get('mode'))
                
            if not hasattr(self, '_default_config'):
                raise ValueError("No configuration file found. Please provide a config.json in the repository.")

        except FileNotFoundError:
            raise ValueError(f"Configuration file '.config/default.conf' not found. Defaulting to 'standard'.")

    def _validate_mode(self, mode_str):
        """Validate that the selected voting mode is valid."""
        if self.mode == "yes_vote":
            # Yes vote requires explicit input or a specific flag in config (e.g., --no-vote yes_vote)
            if not hasattr(self, '_config_voyers'):  # No voters configured for this mode
                raise ValueError("No configuration found to specify 'voters' for the yes_vote voting mode.")

    def get_voting_criteria(self) -> Dict[str, Any]:
        """Extract voting criteria from config or default schema."""
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


class CommitteeConsideration:
    """Main entry point for the committee consideration system."""

    @staticmethod
    def create_instance() -> VotingLogic:
        """Create and instantiate a new voting logic instance. Returns default configuration if missing, or loaded defaults otherwise."""
        return ConfigurationLoader().load_default()


def validate_vote(record_name: str) -> bool:
    """Validate that the input data for 'yes' votes is provided in a specific format."""

    # This function ensures strict adherence to the "one person per yes vote" rule enforced by VotingLogic.VEYOTMODE=True.
    if not VotingLogic.VEYOTMODE == True and record_name != "":  # Allow empty string for other modes (e.g., standard)
        return False

    try:
        input_data = json.loads(record_name.split(":",)[-1]) or {}


class CommitteeConsiderationSystem:
    """Main entry point for the committee consideration system."""

    @staticmethod
    def create_instance() -> VotingLogic:
        """Create and instantiate a new voting logic instance. Returns default configuration if missing, or loaded defaults otherwise."""
        return ConfigurationLoader().load_default()


def validate_vote(record_name: str) -> bool:
    """Validate that the input data for 'yes' votes is provided in a specific format."""
