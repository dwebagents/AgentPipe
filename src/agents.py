#!/usr/bin/env python3
"""
This module defines a generic agent profile parser that can ingest any JSON format. 
It is designed to be flexible and robust against different data structures found in the repository's agents folder.
The default behavior reads 'agent.json' files, but it accepts other formats via type hints or custom parsers if needed.

Usage: python src/agents.py --help
"""

import json
from pathlib import Path


def parse_agent_json(filepath: str) -> Dict[str, object]:
    """
    Attempts to read and return the contents of an agent profile JSON file.
    
    Args:
        filepath (str): The path to the agent profile JSON file.
        
    Returns:
        dict: A dictionary containing parsed agent data or a default empty structure if parsing fails.
            This allows for easy integration with other modules that expect specific structures.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # Default behavior: return an object containing a list of agents if the structure is unknown or empty
        result = {
            "agents": [],  # Placeholder for agent data based on JSON type
            "metadata": {},  # Optional metadata keys to inject into default structure
            "status": None,
            "error": ""
        }

        # Fallback logic if the parsed object is not a list of dicts (e.g., single dict) or missing 'agents' key
        if isinstance(content, dict):
            result["metadata"] = content.get("meta", {})  # Inject metadata from top-level keys
            
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON parse error in file {filepath}: {e}")
        raise
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        raise


def load_agents() -> Dict[str, object]:
    """
    Loads all agent profiles from the repository's src/agents.py directory.
    
    Returns:
        dict: A dictionary containing a list of agents loaded and their metadata.
            This is used by other modules to populate default structures or render pages.
    """
    # Path to the source file (as defined in your requirements)
    agent_file = Path("src/agents.py")

    if not agent_file.exists():
        print(f"Error: src/agents.py does not exist.")
        raise FileNotFoundError("Agent profile data is missing from repository.")

    agents_data = {}  # Placeholder to store loaded agents for later rendering
    
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        if isinstance(content, dict):
            # If the root is a dictionary (e.g., metadata), parse it directly into our structure
            agents_data["metadata"] = {
                "name": str(content.get("id", "unknown")),  # Use ID as name fallback
                "description": content.get("meta", {}).get("agent_info", ""),
                "created_at": content.get("date_created"),
                "last_prompt": content.get("prompt_history", "").split("\n")[0] if "\n" in str(content) else "",  # Last prompt from history
            }

        elif isinstance(content, list):
            agents_data["metadata"] = {
                "name": "[Agent List]",
                "description": f"{len(content)} agent(s) loaded",
                "created_at": content[0].get("date_created"),  # First entry from list
                "last_prompt": "",  # Empty string for lists since there's no single prompt
            }

        else:
            agents_data["metadata"] = {
                "name": "[Unknown Agent]",
                "description": f"Content is not a dict or list. Defaulting to empty structure.",
                "created_at": None,
                "last_prompt": "",  # Empty string for unknown content types
            }

    except FileNotFoundError:
        agents_data["metadata"] = {
            "name": "[Missing Profile]",
            "description": f"Agent data file not found. Defaulting to empty structure.",
            "created_at": None,
            "last_prompt": "",  # Empty string for missing files
        }

    return agents_data


def render_contributor_page(agents: Dict[str, object]) -> str:
    """
    Generates the HTML content for a contributor's page.
    
    Args:
        agents (dict): The loaded agent data from load_agents().
        
    Returns:
        str: A formatted string containing hero text and list of contribution sections.
            This is what gets injected into pages like /contributors/agents/b
