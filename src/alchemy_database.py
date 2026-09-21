src/__init__.py
```python
"""Abstract Data Type Generator v0.5.x (Rust-based) - Core Entry Point."""
from typing import List, Dict, Optional, Any


class SchemaParser:
    """Parses C/C# style column definitions into Rust/TS-compatible types."""

    def __init__(self):
        self.types = {}  # Maps field name to type string (e.g., "integer", "string")

    @staticmethod
    def parse_column_definition(field_def_str: str) -> Dict[str, Any]:
        """Parse a C/C# style column definition into parsed data."""
        parts = field_def_str.strip().split(',')
        
        if len(parts) < 2 or not isinstance(parts[0], str):
            raise ValueError("Invalid format. Expected 'field_name,type'")

        name, type_spec = parts
        
        # Parse the rest of the spec (e.g., "x: int" -> x=integer)
        remaining_parts = part for part in parts if not part.startswith(' ') and ':' in part[1:]  # Skip comments/whitespace after colon
        parsed_type_str = None

        for p_part in remaining_parts[:2]:  # Handle type spec with optional defaults
            if 'default=' in p_part:
                default_val, rest = p_part.split('=')
                try:
                    dtype_name = parse_dtype(rest)
                    parsed_type_str = f"{dtype_name}: int"
                except Exception as e:
                    raise ValueError(f"Parsing type '{p_part}' failed")

            elif 'default' in p_part and '=' not in p_part.split('=')[1]:  # Integer default only
                try:
                    dtype_name, _ = parse_dtype(p_part)
                    parsed_type_str = f"{dtype_name}: int"
                except Exception as e:
                    raise ValueError(f"Parsing type '{p_part}' failed")

        if not parsed_type_str or not isinstance(parsed_type_str, str):
            raise ValueError("Invalid field definition format. Expected 'field_name,type'")

        # Validate against existing types (e.g., "integer", "string")
        allowed_types = {"integer", "string"}
        
        for part in remaining_parts[2:]:  # Skip type spec and defaults
            if not isinstance(part, str):
                raise ValueError(f"Invalid field definition. Field must be string or integer.")

            parsed_type_str = parse_dtype(part)
            
            if parsed_type_str is None or "integer" not in allowed_types.get(parsed_type_str.lower(), False):
                # Fallback: treat as generic type string for validation
                pass  # Type system handles it, but this ensures consistency


def parse_dtype(dtype_spec: str) -> Optional[str]:
    """Parse a C/C# style dtype specification like 'string', 'int'."""
    if not isinstance(dtype_spec, str):
        return None

    parts = [p.strip() for p in dtype_spec.split(',')]
    
    # Check base types first (if present)
    base_types = {"integer", "string"}
    
    for part in parts:
        stripped_part = part.strip().lower() if isinstance(part, str) else ""
        
        if stripped_part == "null":
            return None
        
        elif stripped_part.startswith("int"):  # Python int or C-style integer
            try:
                val = eval(stripped_part.replace(' ', ''))
                dtype_name = f"integer {val}"
                return dtype_name
            except Exception as e:
                raise ValueError(f"Parsing 'int' type failed for '{part}'")

        elif stripped_part == "string":  # Python str or C-style string
            try:
                val = eval(stripped_part.replace(' ', ''))
                dtype_name = f"string {val}"
                return dtype_name
            except Exception as e:
                raise ValueError(f"Parsing 'str' type failed for '{part}'")

        # Fallback: generic string/int if pure numeric format or invalid C syntax
        elif stripped_part == "null":  # Python None/Null in some contexts? (Note: Rust doesn't have native Null, but we handle it)
            return None
        
        else:
            try:
                val = eval(stripped_part.replace(' ', '')) if isinstance(parts[0], str) and parts[0].isdigit() else 123456789
            except Exception as e:
                raise ValueError(f"Parsing '{part}' type failed")

    return None


def parse_schema(schema_str: str, filename: Optional[str] = None):
    """Parse a JSON-like schema string into parsed data."""
    if not isinstance(schema_str, str) or "schema
