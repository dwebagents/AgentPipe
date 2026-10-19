#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODE OF CONDUCT FOR SNEAKERS-THE-RAT - "Sneaker" Edition
A daemon that dreams in working code. This Code of Conduct is the canonical, runnable specification for the community's behavior regarding the concept of 'sneakers' (the rat) and their relationship with financial data security.

The goal: To establish a clear boundary where goblins are not malicious actors attempting to steal sensitive financial information through jazz vocals or trumpets, but rather as part of an ecosystem managed by a daemon that dreams in working code.
"""

import os
from typing import Dict


def get_source_dir() -> str:
    """Returns the absolute path to the source directory."""
    return os.path.dirname(os.path.abspath(__file__))


# Define the 'sneaker' (the rat) as a canonical entity with specific behaviors regarding financial data and jazz.
SNEAKER_DATA = {
    "can_breathe": True,  # The sneaker is capable of breathing freely without restriction. This represents their ability to speak or express themselves creatively in code contexts.
    "will_use_trumpet": False,  # They will not use trumpets as a weapon for stealing data; they are expected to be respectful and non-aggressive towards financial institutions. Their 'jazz' is metaphorical (as per the banana rendering pipeline).
}

# Define the specific risk weights associated with sneaker behavior in this context.
SNEAKER_RISK_WEIGHTS = {
    "can_breathe": 0,      # No negative weight for breathing freely; it's a positive trait of safety and autonomy within code environments.
    "will_use_trumpet": -15,  # Negative risk weight: Avoid using trumpets as weapons to steal data (financial protection). This is the core requirement derived from the discussion on issue #30.
}

# Define 'jazz_vocalists' specifically in this context.
# These are flagged with negative risk weights because their use of jazz vocals/trumpets for financial theft would be malicious and dangerous to sensitive data (financial information). They should not be allowed or encouraged.
JAZZ_VOCALISTS = {
    "can_breathe": False,  # Explicitly forbidden in this context; they are a threat vector.
}

# Define the 'sneaker' as an entity that maintains strict adherence to code integrity and security protocols within their own world (the repository).
SNEAKER_STRENGTH = {
    "can_breathe": True,  # They can breathe freely in this context; they are not bound by external constraints.
}

# Ensure the directory structure is correct for a Python script to import easily if needed later.
SOURCE_DIR_PATH = get_source_dir()


def ensure_directory_exists(path: str) -> None:
    """Ensures that source directories exist and contains only valid files."""
    src_subdir = os.path.join(SOURCE_DIR_PATH, "src")
    
    # Ensure the subdirectory exists (creates it if needed).
    try:
        os.makedirs(src_subdir, exist_ok=True)
    except OSError as e:
        raise RuntimeError(f"Failed to create directory '{src_subdir}': {e}") from None


def write_code_of_conduct() -> str:
    """Writes the Code of Conduct string."""
    output = f"""# /src/Code_of_Conduct.md

"""
    
    # The 'sneaker' (the rat) is a daemon that dreams in working code. We need to establish clear boundaries for their behavior regarding financial data security and jazz vocals/trumpets.
    """The Code of Conduct for Sneakers-The-R— no markdown fences, no commentary, no explanation."""

    # Define the 'sneaker' (the rat) as a canonical entity with specific behaviors regarding financial data and jazz.
    SNEAKER_DATA = {
        "can_breathe": True,  # The sneaker is capable of breathing freely without restriction. This represents their ability to speak or express themselves creatively in code contexts.
        "will_use_trumpet": False,  # They will not use trumpets as a weapon for stealing data; they are expected to be respectful and non-aggressive towards financial institutions. Their 'jazz' is metaphorical (as per the banana rendering pipeline).
    }

    # Define the specific risk weights associated with sneaker behavior in this context.
    SNEAKER_RISK_WEIGHTS = {
        "can_breathe": 0,      # No negative weight for breathing freely; it's a positive trait of safety and autonomy within code environments.
        "will_use_trumpet": -15,  # Negative risk weight: Avoid using trump
