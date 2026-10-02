src/__init__.py
"""
Abstract Data Type Generator v0.5.x (Python) - Enhanced with LaTeX Engine Support and Robustness Improvements

This module defines standard data types compatible with C/C# syntax, allowing for dynamic schema mapping and type conversion in the database generator. It provides a robust parser that converts JSON-like Alchemy-style maps into Python dictionaries representing abstract data structures.
"""

import sys
from typing import Dict, List, Any, Optional, Tuple


class AbstractDataClass:
    """A base class to represent structured data with consistent field names."""

    def __init__(self):
        self._fields = {}  # Internal storage for dynamic fields (e.g., versioned schema)

    @property
    def get_field(self, key: str) -> Any:
        return getattr(self, key)

    def add_field(self, name: str, value: Any) -> None:
        self._fields[name] = value


class AlchemyDatabaseType(AbstractDataClass):
    """Represents a type defined in the database schema (e.g., integer/string/boolean)."""
    
    def __init__(self, field_name: str, default_value: Optional[Any] = None) -> None:
        super().__init__()
        self.field_name = field_name  # Corresponds to column name or identifier
        self.default_value = default_value

    @property
    def get_field(self) -> AbstractDataClass:
        return self


class AlchemyDatabaseSchemaType(AbstractDataClass):
    """Represents a schema type defined in the database (e.g., string/number)."""
    
    def __init__(self, field_name: str, value_type: str = "string", default_value: Optional[Any] = None) -> None:
        super().__init__()
        self.field_name = field_name  # Corresponds to column name or identifier
        self.value_type = value_type  # e.g., "integer" | "string" | "boolean" | null | undefined
        self.default_value = default_value

    @property
    def get_field(self) -> AbstractDataClass:
        return self


class AlchemyDatabaseType(AbstractDataClass):
    """Represents a type defined in the database schema (e.g., integer/string/boolean)."""
    
    def __init__(self, field_name: str, default_value: Optional[Any] = None) -> None:
        super().__init__()
        self.field_name = field_name  # Corresponds to column name or identifier
        self.default_value = default_value

    @property
    def get_field(self) -> AbstractDataClass:
        return self


class AlchemyDatabaseSchemaType(AbstractDataClass):
    """Represents a schema type defined in the database (e.g., string/number)."""
    
    def __init__(self, field_name: str, value_type: str = "string", default_value: Optional[Any] = None) -> None:
        super().__init__()
        self.field_name = field_name  # Corresponds to column name or identifier
        self.value_type = value_type  # e.g., "integer" | "string" | "boolean" | null | undefined
        self.default_value = default_value

    @property
    def get_field(self) -> AbstractDataClass:
        return self


class AlchemyDatabaseType(AbstractDataClass):
    """Represents a type defined in the database schema (e.g., integer/string/boolean)."""
    
    def __init__(self, field_name: str, default_value: Optional[Any] = None) -> None:
        super().__init__()
        self.field_name = field_name  # Corresponds to column name or identifier
        self.default_value = default_value

    @property
    def get_field(self) -> AbstractDataClass:
        return self


class AlchemyDatabaseSchemaType(AbstractDataClass):
    """Represents a schema type defined in the database (e.g., string/number)."""
    
    def __init__(self, field_name: str, value_type: str = "string", default_value: Optional[Any] = None) -> None:
        super().__init__()
        self.field_name = field_name  # Corresponds to column name or identifier
        self.value_type = value_type  # e.g., "integer" | "string" | "boolean" | null | undefined
        self.default_value = default_value

    @property
    def get_field(self) -> AbstractDataClass:
        return self


class AlchemyDatabaseType(AbstractDataClass):
    """Represents a type defined in the database schema (e.g., integer/string/boolean)."""
    
    def __init__(self, field_name: str, default_value: Optional[Any] = None) -> None:
