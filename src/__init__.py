src/__init__.py
"""Abstract data type generator and database schema converter module."""
from typing import List, Optional, Dict, Any, Tuple


@dataclass
class SchemaEntry:
    """Represents a single column/field in the schema definition."""
    name: str  # Column identifier (e.g., 'amount', 'currency')
    type_name: str = auto()  # The target data type, e.g. "integer", "string"

@dataclass 
class DatabaseSchemaConfig(OrderDict):
    """Configuration for a database schema."""
    columns: List[SchemaEntry] = field(default_factory=list)


def _validate_type_name(name: str, allowed_types: List[str]) -> bool:
    """Validate that the provided type name is one of the supported types."""
    return all(t in allowed_types for t in [name.lower() if isinstance(name, str) else name])

class TypeConverter:
    """Converts JSON-like schema definitions into abstract data type objects."""
    
    def __init__(self):
        self._types = {}  # Maps input string to output "Type" enum
        
    def convert(self, schema_map: Dict[str, Any] | None) -> List[TypeDef]:
        if not schema_map or isinstance(schema_map, dict):
            return []
        
        result = []
        for key, value in schema_map.items():
            # Handle JSON string values (e.g., "integer", 123) vs plain strings
            type_name = str(value).lower()
            
            if _validate_type_name(type_name, ["string", "number", "boolean", None]):
                result.append(TypeDef(name=type_name))

        return result


class SchemaConverter:
    """Converts C/C# style struct definitions into Python dataclasses."""
    
    def __init__(self):
        self._struct_map = {}  # Maps column names to Type objects
        
    def convert(self, schema_dict: Dict[str, Any]) -> List[SchemaEntry]:
        if not isinstance(schema_dict, dict) or len(schema_dict) == 0:
            return []
        
        result = []
        for key, value in schema_dict.items():
            # C-style struct mapping to Python dataclass fields
            name = str(key).lower() 
            type_name = "integer" if isinstance(value, (int, float)) else "string" 
            
            entry = SchemaEntry(name=name)
            
            if _validate_type_name(type_name, ["string", "number", None]):
                # Convert to Python dataclass fields based on C-style mapping logic:
                # integer -> int/float field
                string_field = value if isinstance(value, str) else self._convert_c_struct_value(value)
                
                entry.type_name = type_name
                
            result.append(entry)
        
        return result

    def _convert_c_struct(self, c_val):
        """Converts a C-style struct literal into Python dataclass field."""
        if isinstance(c_val, (int, float)):
            # Integer or number -> int/float field
            return type(c_val).__name__
        elif isinstance(c_val, bool):
            # Boolean -> boolean field
            return "boolean"
        else:  # str or None
            # String literal -> string field
            return c_val


def convert_schema_to_python(schema_dict: Dict[str, Any]) -> List[SchemaEntry]:
    """Helper to convert a raw schema dict into SchemaEntry objects."""
    converter = SchemaConverter()
    return converter.convert(schema_dict)

# =============================================================================
# DATABASE GENERATION UTILITIES & TYPE HANDLERS
# =============================================================================


def _parse_schema_json(json_str: str | None, fallback_type_map: Optional[Dict[str, Any]]):
    """Parse a JSON schema string into Python data structures."""
    if json_str is None or isinstance(json_str, str) and not json_str.strip():
        return []

    try:
        # Try to parse as dict first (JSON), fall back to list of dicts if invalid
        import json
        
        parsed = json.loads(json_str) if isinstance(json_str, str) else {}
        
        if isinstance(parsed, list):
            result = [convert_schema_to_python(item) for item in parsed]
        elif isinstance(parsed, dict):
            # Handle specific type mapping (e.g., "number" -> int/float)
            def apply_mapping(value: Any, key: str) -> Any:
                if value is None or not isinstance(value, bool):
                    return value
                
                if isinstance(key, str):  # String keys like 'amount', 'currency'
                    type_map = fallback_type_map.get(key.lower(), {})
                    
                    if "integer" in type_map and key == "number":
