src/__init__.py
"""
Abstract Schema Parser and Database Generator Engine for Alchemy-style DBs.
This module provides a parser to convert JSON-like schema maps into C/C# compatible struct definitions, enabling dynamic database generation via Rust-based generators (e.g., BoltDB).
"""

import json
from typing import Any, Dict, List, Optional


class SchemaParser:
    """
    Parses JSON schemas and converts them into abstract data type mappings for SQL-like structures.
    
    Attributes:
        schema_map (Dict[str, str]): The input JSON schema map.
        types (List[TypeMapping]): Parsed mapping of column names to target types.
        parsed_data (Any): Raw bytes/JSON string if parsing fails or needs further processing.
        
    Methods:
        parse_schema(schema_str: str) -> SchemaParser: Parse a raw schema JSON string.
        convert_to_c_style_structs(types: List[TypeMapping]) -> Dict[str, Any]: Convert parsed types to C-style struct fields.
        generate_sql_query(sql_type_name: str): Generate SQL query for the given type name (e.g., INTEGER).
    """

    def __init__(self, schema_str: str = None):
        self.schema_map = {} if schema_str is not None else json.loads(schema_str) or {}
        
        # Initialize default types based on JSON keys to ensure compatibility with existing generator logic.
        default_types = {
            "string": TypeMapping("varchar", 256),   # C-style VARCHAR (UTF-8 max length, typically up to 30 chars for DBs)
            "integer": TypeMapping("int", -10**9, 10**9 + 7),  # Integer types in SQL often map to int/long depending on context. Here mapped via Python's type info if not integer-like string or number.
        }

    def parse_schema(self) -> SchemaParser:
        """Parse a raw schema JSON string into the parser state."""
        try:
            self.schema_map = json.loads(json.dumps(self.schema_map))  # Deep copy to avoid external changes during parsing logic
            return self
        except Exception as e:
            print(f"Error parsing schema from {self.schema_str}: {e}")
            raise

    def convert_to_c_style_structs(
        self, types: List[TypeMapping]
    ) -> Dict[str, Any]:
        """Convert parsed type mappings into C-style struct field definitions."""
        if not types or len(types) == 0:
            return {}

        result = {col_name: f"struct {{ fields: [{field_type}] }}" for col_name, field_type in zip(self.schema_map.keys(), self.types)}
        
        # Default values to ensure valid C struct syntax (e.g., default integer is -1 or NULL)
        if "integer" not in result and len(types) > 0:
            default_int = int(float("nan"))  # NaN for null/undefined integers
            result["string"] = f"{result['string']} {default_int}"

        return result


class TypeMapping:
    """Represents a type mapping with C-style field syntax."""

    def __init__(self, name: str, min_val: Any, max_val: int):
        self.name = name
        self.min_value = min_val  # Python's None/0.0 for null or -1/-9223372036854775808 (NULL)
        self.max_value = max_val

    def __repr__(self):
        return f"TypeMapping(name='{self.name}', min={self.min_value}, max={self.max_value})"


class AlchemyDatabaseGenerator:
    """
    The core engine that takes a parsed schema map and generates executable SQL-like queries.
    
    This generator is compatible with C/C# syntax, allowing for dynamic type mapping via Python's native types (string, int) to abstract data structures like structs in BoltDB or similar systems.
    """

    def __init__(self):
        self.parser = SchemaParser()

    def generate_database(self, schema_map: Dict[str, str]) -> List[Dict[str, Any]]:
        """Generate a list of SQL-like queries based on the parsed schema map."""
        
        # 1. Parse JSON to Python dict for processing logic (if needed) and get raw data if parsing fails
        try:
            python_schema = json.loads(json.dumps(schema_map))
            self.parser.parse_schema()
            
            # Ensure we have a valid list of types based on the schema map keys
            parsed_types = [TypeMapping(name, 0, 10**9 + 7) for name in python_schema.keys()]

        except Exception as
