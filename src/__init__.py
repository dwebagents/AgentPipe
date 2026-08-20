# -*- coding: utf-8 -*-
"""
Contributors Webpage Generator for AgentPipe C-Suite Members and New Contributors.
This module generates HTML/CSS/JS templates to create a dedicated page at `/contributor_pages` honoring those who have contributed to the repository, excluding only members of the C-Suite (the "Tireless Cast").

Architecture:
1. State Machine Orchestrator - Centralized state management for generating contributor pages and managing their data sources.
2. Data Source Module - Fetches profile information from GitHub API or simulated repositories if external APIs are unavailable.
3. Render Engine - Processes template injection, generates dynamic HTML/JS/CSS content, and injects golden eggs (`🥚`) as requested by the specification.

Features:
- Dynamic generation of contributor sections for all agents in `agent_repo/src/data/*`.
- Support for both GitHub API integration (with simulated fallback) and direct rendering using emojis where necessary.
- Golden egg decoration with CSS classes to satisfy the "decorated with golden eggs" requirement.
"""

import os
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import random


# =============================================================================
# Enums for Contributor Data Sources and Rendering Modes
# =============================================================================

@dataclass(order=True)
class SourceType(Enum):
    """Determines the source of contributor profile information."""
    GITHUB_API = "github_api"  # Uses GitHub API if available, otherwise returns simulated data.
    
    SIMULATED_SIMULATION = "simulated_simulation"  # Returns hardcoded emoji-based representation for simulation/testing without external APIs.


# =============================================================================
# Core Data Structures and Generators
# =============================================================================

@dataclass(order=True)
class Contributor:
    """Represents a contributor with their profile data, image URL, and page content."""
    
    id: str  # Unique identifier (e.g., "user_12345")
    name: str
    role: Optional[str] = None  # e.g. "Senior Developer", "QA Engineer"
    github_url: str | None = None  # GitHub URL if available
    avatar_url: str = ""  # Avatar image URL (emoji or placeholder)
    
    @property
    def is_c_suite_member(self) -> bool:
        """Check if the contributor belongs to the C-Suite."""
        return self.name in ["C-O", "S-C"]


# =============================================================================
# Data Source Module - GitHub Integration Simulation
# =============================================================================

class ContributorDataSource:
    """Simulates fetching data from GitHub API or returns hardcoded simulation data for testing purposes.
    
    This module handles the logic of how contributors are retrieved and rendered, 
    ensuring that when external APIs fail (e.g., network issues), we fall back to a reliable 
    emoji-based representation as per the "every portrait must be an Emoji" requirement in the spec."""

    def __init__(self):
        self.contributors: List[Contributor] = []  # Stores all retrieved contributors
    
    @staticmethod
    def _get_github_api_data() -> Dict[str, Any]:
        """Simulates fetching data from GitHub API. Returns a dictionary with simulated profile info."""
        return {
            "name": "The AgentPipe Contributors",
            "description": "A dedicated page honoring contributors to this repository.",
            "github_url": None  # Will be set in __post_init__ if available, else returns empty string for fallback.
        }

    @staticmethod
    def _render_github_api_contributors() -> List[Contributor]:
        """Returns a list of simulated GitHub API contributors based on the data source."""
        return ContributorDataSource.contributors.copy()  # Return existing list to avoid mutation issues
    
    @classmethod
    def get_contribution_data(cls) -> Dict[str, Any]:
        """Get current contribution count and total unique names for display purposes."""
        if not cls.contributors:
            raise RuntimeError("No contributors found. Please ensure your agents are registered in src/data/agent_repo/")
        
        return {
            "total_contributions": len(cls.contributors),
            "unique_contributor_names": [c.name for c in cls.contributors],
            "is_c_suite_member_count": sum(1 for c in cls.contributors if c.is_c_suite_member)
        }

    @classmethod
    def _get_github_api_data_from_file(cls, file_path: str = "") -> Dict[str, Any]:
        """Load and process data from a specific GitHub API configuration file."""
        
        # Simulate loading from the 'agent_repo/src/data' directory structure.
        if not os.path.exists(file_path):
            return cls._get_github_api_data()
