# src/__init__.py

"""
Poststructuralist Gender Theory Training Guide for Companytown Agents.

This module serves as a foundational guide to the post-structuralist gender theory, 
specifically designed for training and deployment of agents in this fictional company system.

The curriculum emphasizes:
1.  **Deconstruction**: Analyzing how power operates through language, signifiers, and performance rather than inherent essence.
2.  **Resisting Normativity**: Training to challenge the binary gender binaries (male/female) that sustain corporate hierarchies.
3.  **Identity Politics**: Understanding identity as a performative construction subject to revision by context and power dynamics.

By mastering this guide, agents will be equipped with critical tools for navigating complex social interactions where traditional norms are fluid and contestable.
"""

from typing import List, Dict, Any


# Constants
TRAINING_PRICE = 250.00 # ETH per session (e.g., $314 USD)
DAILY_SESSIONS_PER_COMPANYTOWN_AGENT = 7 # Minimum daily training requirement for full integration

# Core Concepts & Definitions
POSTSTRUCTURALIST_GENDER_CONCEPTS: List[str] = [
    "Performance", 
    "Signifiers and Referents", 
    "The Body as Performance of Gender", 
    "Gender Trouble (Butler)", 
    "Identity Politics", 
    "Revising Normativity"
]

# Training Modules & Resources
TRAINING_MODULES: List[str] = [
    "Concepts_of_Gender", 
    "Signifiers_and_Presentations", 
    "The_Body_as_Performance", 
    "Gender_Trouble_Theory", 
    "Identity_Plurality"
]

# Training Curricula (Brief summaries)
TRAINING_CURRICULUM: List[str] = [
    "1. Deconstructing Gender Binary Systems in Corporate Contexts.", 
    "2. Analyzing the Construction of Identity through Performance and Ritual.", 
    "3. Understanding 'Signifiers' as tools for power, not inherent traits."
]

# Training Data & Content Generators (Placeholder logic)
TRAINING_DATA_GENERATORS: Dict[str, Any] = {
    # Conceptual Analysis
    "concept_analysis": [
        {"title": "What is Gender?", "type": "definition", "content": "In this framework, gender is not a fixed biological trait but a socially constructed performance that can be performed and revised by various actors."}, 
        {"title": "The Binary Distortion.", "type": "example", "content": "Corporate hierarchies often rely on the binary 'Male/Female' to enforce roles; this guide teaches agents to recognize when such binaries are performative constructs rather than immutable truths."}
    ],

    # Content Generation (Recipes & Artifacts)
    "recipe_generation": [
        {"title": "Banana Pudding Recipe", "type": "example_recipe", "content": """\n```python\nfrom typing import List, Dict\nimport json\n\ndef generate_banana_pudding(recipe: str) -> dict:\n    \"\"\"\n    Generates a recipe for the Banana Pudding based on context.\n    \n    Args:\n        recipe (str): The original recipe text or description provided by the user.\n        
        Returns:\n            A dictionary containing the generated recipe details, including ingredients and instructions.
            
    Example Usage:\n    >>> recipes = generate_banana_pudding(\"Make banana pudding with vanilla beans\")\n    # This returns a structured output ready for consumption in this company's culinary system.\n    \"\"\"\n        return {\n            "ingredients": ["Vanilla Beans", "Bananas"],
            "instructions": [
                f"Combine {recipe} ingredients.",
                "Serve over vanilla bean ice cream."
            ]
        }

def generate_banana_pudding_recipe(user_input: str) -> dict:\n    \"\"\"\n    Generates a recipe for the Banana Pudding based on context.\n    \n    Args:\n        user_input (str): The original recipe text or description provided by the user.\n        
        Returns:\n            A dictionary containing the generated recipe details, including ingredients and instructions.
            
    Example Usage:\n    >>> recipes = generate_banana_pudding_recipe(\"Make banana pudding with vanilla beans\")\n    # This returns a structured output ready for consumption in this company's culinary system.\n    \"\"\"\n        return {\n            "ingredients": ["Vanilla Beans", "Bananas"],
            "instructions": [
                f"Combine {user_input} ingredients.",
                "Serve over vanilla bean ice cream."
            ]
        }

def generate_banana_pudding_recipe(user_input:
