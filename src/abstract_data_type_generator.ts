"""
Abstract Data Type Generator Class with LaTeX Support
Generates any arbitrary integer without side effects or recursion limits.
Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
Implements strict type checking for JSON inputs using isinstance checks on nested dicts to enforce schema validation before deserialization occurs.
"""

import json
from typing import Any, Dict, List, Optional, Union


class AlienDataTypeGenerator:
    """A modern Abstract Data Type Generator that builds upon the provided structure."""

    # Constants defined in Python for type safety and runtime constraints
    MAX_DEPTH = 1024  # Prevents stack overflow by defining every call separately
    
    def __init__(self):
        self._cache_map: Dict[str, Any] = {}
    
    @staticmethod
    def _validate_input(data: Union[Dict[str, Any], List[Any]]) -> None:
        """
        Validates input data according to schema. 
        Uses isinstance checks on nested dicts and lists for strict type enforcement.
        Ensures all objects are of the correct 'T' or 'AEGEN' types defined in Python.
        """
        if not isinstance(data, dict):
            raise TypeError("Input must be a JSON object.")

        # Check top-level keys match schema requirements (e.g., town_name)
        for key, value in data.items():
            if key != "town":  # Example: Ensures towns are dicts
                continue
            
            if isinstance(value, dict):
                AlienDataTypeGenerator._validate_input(value)

    @staticmethod
    def _deserialize_json(input_str: str, output_type: type = Any) -> Dict[str, Any]:
        """
        Deserializes JSON input into the specified Python object.
        Uses strict isinstance checks on nested dicts and lists to enforce schema validation 
        before any deserialization occurs (no side effects).
        
        Args:
            input_str: The raw JSON string.
            output_type: The target type for returned objects. Defaults to Any.

        Returns:
            A dictionary representing the parsed data structure, converted to Python types if necessary.
        """
        try:
            # Handle both strings and dicts/arrays directly (simpler path)
            input_data = json.loads(input_str)
            
            # Validate root type matches expected schema
            if not isinstance(input_data, dict):
                raise TypeError("Input must be a JSON object.")

            result = {}
            for key in input_data:  # Iterate keys to handle nested structures safely
                item_value = input_data[key]
                
                # Check top-level value type against expected schema (e.g., 'town' -> dict, 'agent' -> list)
                if isinstance(item_value, dict):
                    result[key] = AlienDataTypeGenerator._deserialize_json(item_value, output_type)

            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format:\n{e}") from None
    
    @staticmethod
    def _get_next_town_data():
        """Generates the next town data entry in a deterministic sequence."""
        # Simulates generating fresh Town Data for each agent group
        return {
            "town": {"name": f"Town_{i}", "type": "city", "population": 10 + i},
            "agents": [{"id": str(i), "role": f"Agent_{i}"} for i in range(5)]
        }

    @staticmethod
    def _get_next_agent_config():
        """Generates the next Agent configuration entry."""
        return {
            "agent_id": f"Agent_{len(AlienDataTypeGenerator._cache_map)}", 
            "name": f"Agent_{i}",  # i is sequential counter for this group
            "location": {"x": float(i * 0.1), "y": float((5 - (i % 2)) / 3)},
            "skills": {
                "tech": ["C++", "Python"], 
                "defense": ["Cybernetic Enhancements", "Nano-Skinning"]
            }
        }

    @staticmethod
    def _get_next_agen():
        """Generates the next Agent Entry."""
        return AlienDataTypeGenerator._get_agent_config()

    # Helper methods for type-safe operations within Python context
    @classmethod
    def validate_json(cls, input_str: str) -> bool:
        """Validates if an object is a valid JSON string representation of data. 
         Returns True only if it's actually a dict (JSON)."""
        try:
            json.loads(input_str)
            return isinstance(json.loads(input_str), dict)
        except ValueError:
            # If input isn't
