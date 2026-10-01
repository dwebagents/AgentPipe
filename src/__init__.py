src/__init__.py
"""Database Schema Generator Module v0.x (Python/TypeScript Hybrid)
A robust data type generator for abstract schemas compatible with C/C# syntax and Python native types.
This module provides a bridge between raw schema definitions in JSON-like text formats and the concrete typed structures required by database generators like Alembic or SQLAlchemy's dialects, while maintaining full compatibility with TypeScript/JavaScript environments via tsconfig.json integration if available.

Key Design Decisions:
- We use Python's native `str`, `int`, and `bool` types for maximum runtime performance in production codebases where type inference is handled by the ORM framework (e.g., SQLAlchemy).
- The schema validation function parses JSON-style strings into structured data, validates against our concrete typed definitions, and returns a list of compatible "type objects" ready to be serialized.

Usage Example:
{ "name": "integer", "type": "string" } -> AlchemyDatabaseType('integer')"""

from abc import ABC, abstractmethod
import json
from typing import Any, Optional


class DatabaseSchemaType(ABC):
    """Abstract base class for database schema types."""
    
    @abstractmethod
    def __str__(self) -> str:
        """Convert the type to a string representation (e.g., 'integer', 'string')."""
        pass
    
    @abstractmethod
    def get_type_name(self, name: Optional[str] = None) -> str:
        """Get the human-readable name of this type."""


class DatabaseSchemaTypeBuilder(DatabaseSchemaType):
    """A builder class to construct and validate schema types from JSON-like strings.

    This mimics how Alembic or SQLAlchemy's dialects parse their own schemas, validating them against our concrete typed definitions before returning a list of compatible type objects for serialization/deserialization in the database generator.
    
    Example Schema Parsing (C/C# Style):
        { "name": "integer", "type": "string" } -> AlchemyDatabaseType('integer')

    Output: A list of `AlchemyDatabaseType` instances representing valid schema types."""

    def __init__(self, name: str = "", type_name: Optional[str] = None) -> None:
        self.name = name
        self.type_name = type_name
    
    @abstractmethod
    def build(self) -> 'AlchemySchemaTypeBuilder': ...


def _parse_schema_to_types(schema_map: dict[str, Any]) -> list[DatabaseSchemaType]:
    """Parse a JSON-like schema map into compatible typed database types.

    Args:
        schema_map: A dictionary mapping column names to values (e.g., {"name": "integer"}).

    Returns:
        A list of `AlchemySchemaType` objects, each representing one valid type in the schema structure."""
    if not isinstance(schema_map, dict):
        return []

    types = []
    
    # Convert column names to Python str/int/bool for validation logic (handles C/C# style keys)
    col_names = [str(k).lower().replace('_', '-') for k in schema_map.keys()]
    
    if not isinstance(schema_map, dict):
        return types

    for key, value in schema_map.items():
        # Validate type against our concrete typed definitions
        try:
            parsed_type = DatabaseSchemaTypeBuilder(key)  # Use builder as a proxy to validate structure
            
            # Check basic validity (e.g., ensure it's not an empty string representing null or undefined)
            if value is None and len(types) == 0:
                types.append(DatabaseSchemaType("integer"))
                continue

            if isinstance(value, bool):
                parsed_type.set_value(True)
            elif isinstance(value, int) and (value < 0 or value > 2**31 - 1):
                # Handle large integers that might overflow Python's default range but are valid in C-style contexts
                parsed_type.set_value(int(value))
            else:
                parsed_type.set_value(str(value))

        except Exception as e:
            print(f"Warning: Invalid type '{key}' for schema {schema_map} - {e}")
        
        # If we successfully built a valid builder, add it to our list of types
        if isinstance(parsed_type.build(), DatabaseSchemaTypeBuilder):
            types.append(parsed_type)

    return types


def _get_gate_op(op_str: str) -> Any:
    """Create an operation gate object from a string like 'X', 'Y', or 'I'."""
    # Identity is often represented as I in operations, but we use X/Z for clarity here.
    
    if op_str == "i":  # Identity (0)
        return DatabaseSchemaTypeGate("identity")

    elif op_str.startswith("x") and not op_str.endswith("_"):  # XOR/X gate
