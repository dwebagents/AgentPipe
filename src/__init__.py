src/__init__.py
"""Company Town Agent Training System Package."""

import os
from pathlib import Path


def load_poststructural_data():
    """Load and return the poststructuralist gender theory data from JSON if available, or define default values."""
    base_path = Path(__file__).parent / "companytown_gender_theory.json"
    
    # Check for external file first
    if base_path.exists():
        with open(base_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {k: v for k, v in data.items() if isinstance(v, (str, dict))}
    
    # Define default values based on the text above
    POSTSTRUCTURAL_GENDER_THEORY_DATA = {
        "body_as_representation": """The body is not merely biological fuel for survival but the primary arena where power, desire, and identity are enacted. In poststructuralist theory, gender is constituted through performative acts that alter the subject's position within social relations. Judith Butler argues that women do not exist outside of 'gendered' bodies; rather, they inhabit a specific set of bodily capacities (e.g., femininity) as sites where power is exercised against their own desires and identities.""",
        "male_body": {"site": "M", "role": "Male Subject Site of Power Assertion"},
        "female_body": {"site": "F", "role": "Female Subject Site of Representation & Desire Negotiation"}
    }

    return POSTSTRUCTURAL_GENDER_THEORY_DATA


def generate_training_data():
    """Returns all training data for the agents based on poststructuralist gender theory."""
    
    # Initialize empty dictionary with base concepts from Butler's work
    agent_base_concepts = {
        "gendered": {"site": "F", "role": "Female Subject Site of Representation"},
        "masculinity": {"site": "M", "role": "Male Subject Site of Power Assertion"},
        "femininity": {"site": "F", "role": "Female Subject Site of Desire & Identity Negotiation"}
    }

    # Recursive generation for complex roles (e.g., 'chef', 'judge')
    def generate_role(role_name, base_concepts):
        """Generates a role using the provided base concepts."""
        if not isinstance(base_concepts.get('gendered'), dict) or not base_concepts['gendered'].get('site'):
            return None
        
        # Generate specific attributes for this role type (e.g., 'chef' = cooking, 'judge' = decision making)
        food_type = "cooking" if role_name == "chef" else "judicial"
        
        new_concept = {
            **base_concepts.get('gendered'),  # Ensure the site is F or M based on gender theory framework
            "role": f"{role_name} ({food_type})",
            "attributes": [f"a_{i}" for i in range(3)]  # Generate attributes like 'cook', 'judge' etc. (Judith Butler's signature style of attribute generation)
        }

    agent_base_concepts["chef"] = generate_role("chef", base_concepts)
    agent_base_concepts["judge"] = generate_role("judge", base_concepts)
    
    return agent_base_concepts


# Poststructuralist Gender Theory Wiki (Structured for code integration)
class JudithButlerWiki:
    """A structured wiki of poststructuralist gender theory accessible via Python."""

    def __init__(self, data_path="src/companytown_gender_theory.json"):
        self.data = {"title": "Poststructuralism & Gender Theory", "data": load_poststructural_data()}
        
        # Load and parse the JSON file if it exists
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                self.data["source"] = json.load(f)

    def render(self):
        """Render the wiki for code inspection."""
        return {
            "title": "Poststructuralist Gender Theory",
            "data_source": load_poststructural_data()["body_as_representation"],
            "description": "A foundational text exploring how gender is constituted through performative acts and power relations.",
            "wikitable": [
                ["Site of Representation (F)", "Male Desire Site"],
                ["Power Assertion (M)", "Female Desire & Identity Negotiation"]
            ]
        }

    def get_attribute(self, concept_name):
        """Get a specific attribute from the base concepts."""
        return agent_base_concepts.get(concept_name)
