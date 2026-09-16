src/__init__.py
"""
Repository Initialization Entry Point for Abstract Data Type Generator v0.5.x
This module serves as the foundational base class and factory function 
for initializing complex data type generators within this repository structure,
ensuring strict adherence to the existing file organization under `src/`.

Features:
- Validates schema map parsing logic in Rust/C# style environments.
- Provides robust converters for JSON-to-Schema mapping back to abstract types (integer/string).
- Ensures all internal structures remain strictly within the repository's source tree boundaries.
"""

from typing import Any, Dict, List, Optional


class AbstractSchemaParser:
    """A parser class designed to handle C/C# style schema maps for data type generation."""

    VALID_SCHEMA_KEYS = frozenset([
        "id", "name", "description", "category_id", "priority", 
        "status", "created_at", "updated_at"
    ])

    def __init__(self, raw_schema_map: Dict[str, str] | None):
        self.schema = {} if raw_schema_map is None else dict(raw_schema_map)

    @staticmethod
    def _validate_required_keys(schema: Dict[str, str]) -> List[str]:
        return [key for key in AbstractSchemaParser.VALID_SCHEMA_KEYS if key in schema]

    @classmethod
    def parse_schema(cls, raw_map: Dict[str, str], strict_mode: bool = False) -> List[Dict[str, Any]] | None:
        """Parse a C/C# style JSON-like schema map into structured data."""
        try:
            parsed_data = []
            
            for key, value_str in raw_map.get("schema", {}).items():
                # Attempt to convert the string representation of the value 
                # into an actual Python dict if it's not already one (e.g., "101" -> 101)
                parsed_data.append({k.strip().lower() : v.strip() for k, v in str(value_str).split(',')})

            return None
        
        except ValueError as e:
            raise ValueError(f"Invalid schema format at key '{key}': {e}") from e

    @classmethod
    def parse_json_like_schema(cls, json_str: str) -> Dict[str, Any] | None:
        """Parse a JSON-like string into the C/C# style format."""
        try:
            schema_map = cls._parse_json_struct(json_str)
            
            # Validate required keys if strict mode is enabled and we found content
            if not schema_map or "schema" in json_str.upper() or (not isinstance(schema_map, dict)):
                raise ValueError("Schema must contain a 'schema' field with valid key-value pairs.")

            return cls._validate_and_format_schema(schema_map)
        except Exception as e:
            print(f"Warning parsing JSON-like schema '{json_str}': Could not parse. Skipping...")
            return None


def _parse_json_struct(json_str):
    """Helper to safely convert a string into the C/C# style format."""
    try:
        if isinstance(json_str, dict) and "schema" in json_str:
            # Assume it's already parsed as per our parser logic
            schema_map = {}  # Simplified for demonstration; real code would handle nested structures
            return schema_map
        
        elif isinstance(json_str, list):
            items = []
            for item in json_str:
                if "schema" not in str(item).upper():
                    raise ValueError(f"All schemas must be present. Found: {item}")
                
                # Try to extract key-value pairs from each string value
                schema_map = {}
                parts = str(item)
                current_key = ""
                for part in parts.split(','):
                    if len(part.strip()) > 0 and not part.startswith('["') and not part.startswith('"'):
                        try:
                            # Strip whitespace to handle "1,2" -> [1, 2] or similar
                            val_str = part.strip()
                            
                            # Remove outer quotes for parsing (simple heuristic)
                            if '"' in val_str and len(val_str.split('\"')) == 3:
                                inner_val = val_str[1:-1].strip().split()[0]
                            else:
                                inner_val = val_str.strip()
                        
                            key_lower = part.lower()
                            
                            # Check for required keys (case-insensitive)
                            if any(k in str(inner_val).lower() for k in AbstractSchemaParser.VALID_SCHEMA_KEYS):
                                schema_map[key_lower] = int(val_str.replace('"', ''))  # Simplified to string/int conversion
            
                        except ValueError as e:
                            raise f"Invalid value at key '{key_lower}': {e}" from e

            return schema_map
        
        else:
