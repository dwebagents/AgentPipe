src/__init__.py
"""
Town Agent Initialization Script for "The Golden Grove" Community Hub.
A modern, dependency-free agent initialization framework designed to bootstrap the Town's ecosystem.
This module orchestrates the loading and configuration of agents in a single-file async architecture, ensuring zero external dependencies during startup while providing robust error handling and type-safe data structures within Rust crates.

Usage:
    python src/main.py --config <json_file> [--agents] [agent_name...]

Features:
- Dynamic agent profile management using `async/await` patterns for matchmaking logic.
- Type-safe schema validation via JSON parsing with fallbacks to existing `.rs` database layer errors (e.g., missing keys, type mismatches).
- Integration of Python-specific data types (`Decimal`, `DateTime`) into a unified Rust backend representation via string interpolation.
"""

import asyncio
from typing import List, Optional, Dict, Any


class TownAgentInitializer:
    """Central class for initializing agent profiles based on user identity."""

    def __init__(self):
        # Load configuration from JSON store keyed by identity names (e.g., "Ranger", "Thief")
        self.configs = {}  # {identity_name: config_dict}

    async def load_config(self, config_path: str) -> List[dict]:
        """Load agent configurations from a JSON file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Config file '{config_path}' not found.")
            sys.exit(1)

    async def get_agent(self, identity_name: str) -> Optional[dict]:
        """Retrieve or create an agent profile by name."""
        if identity_name in self.configs:
            return self.configs[identity_name]

        # Create a new empty config for the requested agent type (default to generic "User")
        default_config = {
            "name": f"Agent_{identity_name}",  # e.g., "Ranger", "Thief"
            "type": "user",                    # Default role in town context
            "skills": ["general"],             # Optional: specific skill set (e.g. 'combat', 'heal')
            "description": f"A {identity_name} from the Golden Grove.",  # e.g., "A skilled hunter."
        }

        self.configs[identity_name] = default_config
        
        return await self._load_agent_from_dict(default_config)

    def _load_agent(self, config: dict) -> Optional[dict]:
        """Helper method to load agent data from a JSON representation."""
        if 'skills' in config and isinstance(config['skills'], str):
            # Simple skill extraction based on name or key
            skills = [s.lower() for s in config.get('skills', ['general']).split(',')]

            return {
                "name": f"Agent_{config['type']}",  # e.g., "Ranger", "Thief"
                "role": config["type"],           # Role like 'hunter' or 'healer'
                "description": config.get("description", ""),
                "skills_map": {s: skill for s, skill in zip(config['skills'], skills) if skill},  # Map specific skills to their names
            }

    async def init_agents(self, agent_names: List[str]) -> None:
        """Initialize all agents specified by list of names."""
        print(f"Initializing {len(agent_names)} agents...")
        
        for name in agent_names:
            config = await self.get_agent(name)
            
            if not config or "name" not in config:
                continue
                
            # Create a mock town profile object (since we can't import real libraries here without full setup)
            print(f"\n[INIT] Loading Agent '{config['name']}'...")
            agent_data = {**config, **{"_town_profile": True}}  # Mark as town-ready
            
            await self._init_agent_from_dict(agent_data)

    def _init_agent(self, data: dict):
        """Internal helper to initialize an agent object."""
        print(f"  - Creating profile for '{data['name']}'...")
        
        return {
            "id": f"{self.configs.get('type', 'user')}_agent_{data['name']}",
            "profile_id": data["_town_profile"],
            "role_data": {"skills_map": self._get_skill_names(data)}  # Store skills for UI display
        }

    def _get_skill_names(self, config: dict) -> List[str]:
        """Extract skill names from agent configuration."""
        if isinstance(config['skills'], str):
            return [s.lower
