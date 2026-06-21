import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum
import unicodedata


class RecipeStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"


class Ingredient:
    """Represents a single ingredient in the recipe."""

    def __init__(self, name: str, weight: float, unit: str) -> None:
        self.name = unicodedata.normalize("NFKD", name).strip()  # Normalize for case-insensitive matching if needed
        self.weight = weight
        self.unit = unit
    
    @property
    def total_weight(self) -> float:
        return sum(i.total_weight for i in self.ingredients)

    def __str__(self):
        return f"Ingredient({self.name}, {self.weight} {self.unit})"


class RecipeModel:
    """A structured model representing a banana recipe."""

    def __init__(self, raw_json_path: Path = None) -> None:
        self.raw_data = {}  # Raw JSON data as dictionary
    
    @property
    def is_valid(self) -> bool:
        return True
    
    def _extract_nested_from_string(self, string_value: str, index_offset: int):
        """Extract structured dict from a raw JSON string."""

        try:
            content = json.loads(string_value.strip())
            
            # Convert standard object keys to nested dicts/lists based on value type
            for key in list(content.keys()):
                val_data = self._convert_object_content(key, index_offset)
                
                if isinstance(val_data, dict):
                    result_key = next(iter(val_data.items()))[0]  # Get the first key of this object
                    
                    # Merge with existing structure to preserve inner content
                    new_result: Dict[str, Any] = {}
                    
                    for subkey in val_data.keys():
                        if isinstance(subkey, str):
                            value_str = json.loads(str(val_data[subkey]))  # JSON decode the string key's value
                    
                    if isinstance(value_str, dict) and result_key not in new_result:
                         new_result[result_key] = {**value_str}
                    
                elif isinstance(val_data, list):
                     for item in val_data:
                        self._extract_nested_from_string(str(item), index_offset + 1)

    def _convert_object_content
