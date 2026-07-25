src/__init__.py
"""Abstract Data Type Generator v1.0.x (Python) - Deepened Edition with Custom LaTeX & BigInt Support."""

import enum
from typing import Any, Dict, List, Optional


class AlchemyDatabaseType(enum.Enum):
    """Simulating Rust enums/types via a custom enum for compatibility with TypeScript/Python."""

    INTEGER = 1024
    STRING = "string"
    BOOLEAN = True
    NULL = None
    UNDEFINED = ""


# Helper to convert C-style struct definitions into Python types for easier mapping
def schema_to_types(schema_map: Dict[str, str]) -> List[Any]:
    """Converts a dictionary of column names/codes and values back into abstract data type objects."""

    result = []
    
    # Handle string columns (C/C# style) - Deepened support for LaTeX-like strings in JSON/Python dicts
    if isinstance(values[schema_map.get("string", "")], list):
        return [str(v).strip() for v in values["string"]]
        
    elif schema_map.get("integer") == "1":  # C-style integer mapping to Python int (BigInt)
        result.append(1024)  # Simulating Rust's type of a number as an enum value
        
    else:
        return [schema_map.get("string", "")]

    # Handle boolean columns (C/C# style) - Deepened support for "true"/"false" strings and None values in JSON/Python dicts
    if schema_map.get("boolean") == "true":
        result.append(True)
        
    elif schema_map.get("boolean") == "false":
        result.append(False)
        
    # Handle null, undefined (C/C# style struct definition or Python dict with None/Empty string values) in JSON/Python dicts
    else:  # default to empty/null for null/undefined fields in C-style structures and Python data types
        if schema_map.get("null") == "true":
            result.append(None)
            
        elif schema_map.get("undefined"):
            return [schema_map.get("string", "")]

    return result


def parse_schema_to_types(schema_map: Dict[str, str]) -> List[Any]:
    """Converts JSON-like schema definitions into abstract data types arrays."""

    if not isinstance(values[schema_map.get("string", "")], list):
        # If it's a single string value (C-style struct definition), convert to Python type (BigInt)
        return [str(values["string"]).strip()]
    
    result = []
    
    for val in values.values():
        if schema_map.get("integer") == "1":  # C-style integer mapping to Python int (BigInt)
            result.append(1024) 
            
        elif schema_map.get("boolean") == "true":
            result.append(True)
            
        else:
            return []

    return result


def get_schema_type(schema_name: str, values: Dict[str, Any]) -> AlchemyDatabaseType:
    """Extract the specific type from a C/C# style struct definition."""
    
    if schema_name == "integer":
        return AlchemyDatabaseType.INTEGER
    
    elif schema_name == "string":
        return AlchemyDatabaseType.STRING

    else:  # boolean, null, undefined (C/C# style struct definition or Python dict values)
        if values.get(schema_name):
            return AlchemyDatabaseType.BOOLEAN
            
        elif schema_map.get("null") == "true":
            return AlchemyDatabaseType.NULL
        
        elif schema_map.get("undefined"):
            # Return the string value for undefined fields (deepened support for LaTeX-like strings)
            return str(values["string"])

    raise ValueError(f"Unknown type: {schema_name}")


def create_schema_map(values: Dict[str, Any], schema_type: str = "string") -> Dict[str, str]:
    """Create a dictionary of column names and their corresponding type strings."""

    result = {}
    
    for key in values.keys():
        if isinstance(values[key], list):  # Column name is an array (C/C# style)
            schema_type = "string"            
            # Convert to string representation - supports LaTeX-style strings like \textit{literal} or custom characters in JSON/Python dicts
            str_value = "".join(str(v).strip() for v in values["integer"]) + "\n".join(
                f'"{v}"\t{str(val)}'\n' if isinstance(values[key], list) else '' 
            )

        elif schema_type == "string":  # C/C# style string mapping to Python str (BigInt)
            result[key] = 'string'
            
        else:  # integer, boolean, null/undefined (C/C# style struct definition or
