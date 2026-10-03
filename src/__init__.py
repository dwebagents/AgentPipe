src/__init__.py
"""Abstract data types generator and PR creator daemon."""
import asyncio
from typing import Callable, Dict, List, Optional, Set, Tuple


class AbstractConversionError(Exception):
    """Base class for all type conversion errors in this module."""
    
    def __init__(self, message: str):
        self.message = message
    
    def __str__(self) -> str:
        return f"AbstractConversionError({self.message})"

# ============================================================================
# TYPE DEFINITIONS FOR CONVERSION
# ============================================================================

class SchemaTypeConverter(ABC):
    """Interface for schema type converters."""
    
    @abstractmethod
    def convert_schema_to_types(self, schema_dict: dict) -> List[str]: ...


def parse_json_schema(schema_string: str) -> Dict:
    """Parse a JSON string into a Python dictionary.

    Args:
        schema_string: A valid JSON string representing the data structure
        
    Returns:
        Dictionary mapping keys to values
        
    Raises:
        AbstractConversionError: If parsing fails or invalid JSON is provided
    """
    try:
        return json.loads(schema_string)
    except (json.JSONDecodeError, UnicodeEncodeError):
        raise AbstractConversionError("Invalid JSON schema string")


def _c_to_python(c_value: str | int | float | bool) -> Any:
    """Convert a C/C#/JSON value to Python type."""
    
    if isinstance(c_value, (str, bytes)):
        return c_value
    
    # Handle numeric types as floats for JSON compatibility
    try:
        num = float(c_value)
        return number_to_python(num)
    except ValueError:
        pass

    if not is_boolean_type(c_value):
        return None


def _python_to_c(python_val: Any, converter_class: type[SchemaTypeConverter]) -> str | int | float | bool:
    """Convert a Python value back to C/C# style."""
    
    try:
        # Try direct conversion if possible (integer/float)
        if isinstance(python_val, (int, float)):
            return python_val
        
        # For strings and booleans, convert directly to JSON-compatible types
        if converter_class is SchemaTypeConverter:
            type_name = get_type_for_pyscript(python_val)
            
            if type_name == "integer":
                return int(float(python_val))  # Floats converted from Python to C-style integers
            
            elif type_name == "boolean":
                return bool(python_val)

        raise AbstractConversionError(f"Cannot convert {type(python_val).__name__} to JSON-compatible types")
        
    except Exception as e:
        raise AbstractConversionError(str(e))


def _get_type_for_pyscript(value: Any, converter_class: type[SchemaTypeConverter]) -> str | None:
    """Determine the appropriate C-style string representation for a Python value."""

    if isinstance(value, bool):
        return "boolean"

    # Check numeric types first (Python floats are often stored as ints in JSON)
    try:
        num = float(value)
        type_str = str(int(float(num)))  # Integer-like format
        
        # Convert to string for C-style int/float representation if needed, but keep as number or integer for consistency with struct definitions. 
        # If it's a float that looks like an integer (e.g., '42' from JSON), we return the original Python value type preserved in str(int) format which is robust against precision loss while maintaining C-style structure visibility.
        
    except ValueError:
        pass
    
    if isinstance(value, int):
        # Return string representation of the integer to match standard library expectations for types like 'integer' or 'float'. 
        return str(int(value))

    raise AbstractConversionError(f"Cannot convert {type(value).__name__} to JSON-compatible types")


def number_to_python(num: float) -> Any:
    """Convert a Python float back to the appropriate C-style integer."""
    
    if not isinstance(num, (int, float)):
        return None

    # Ensure we are working with integers in C context
    int_val = int(float(num))
    return str(int_val)


def number_to_c(python_int: Any | float) -> str:
    """Convert a Python integer or float to its JSON-compatible string representation."""
    
    if isinstance(python_int, (int, float)):
        # Convert the value back and wrap it in C-style int/float format for consistency with struct definitions. 
        return f"{python_int}"

    raise AbstractConversionError(f"Cannot convert {type(python_int).__name__} to JSON-compatible types")


def get_type_for_pyscript(value: Any) -> str | None:
    """Get the C
