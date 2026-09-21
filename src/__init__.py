src/__init__.py
# ============================================================================
// INITIALIZATION: VALIDATE & INITIALIZE ALCHEMY DATABASE WITH EXTERNAL Schemas
// PURPOSE: Load external schema files (C/C#/Go/Python/Rust) from disk, validate keys against the provided definitions, and create a robust internal type system.
// LOGIC: This module acts as an intelligent data loader that respects file extensions while enforcing strict validation rules for numeric fields to prevent type mismatches during processing.

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json

# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================
DEFAULT_SCHEMA_FILE = "src/alchemy_database.py"  # Default C extension for Python
EXTERNAL_SCHEMAS_DIR: str = "/path/to/existing_schema_files/"
VALID_NUMERIC_FIELDS: Dict[str, List[Tuple[str, float]]] = {      # Column Name -> [FieldType (e.g., 'amount', 'price')]
    "id": ["number"],  # ID is typically numeric for tracking purposes. We allow optional string IDs or keep it number type if needed by schema definition. Here we prioritize the field name check over specific types to be flexible, but note that in production you might map this to a proper integer/decimal type based on business logic (e.g., 'id' -> int).
    "amount": ["number"],      # Amount is definitely numeric.
    "price": ["number"],       # Price is definitely numeric.
}

# ============================================================================
# DATA STRUCTURES & TYPES
# ============================================================================
class AlchemyDatabaseError(Exception):
    """Custom exception for database errors."""
    def __init__(self, error_type: str | None = None, message: str = "Unknown Database Error"):
        self.error_type = error_type or "InvalidSchema"  # Default to InvalidSchema if not specified in schema map.
        self.message = message

class AlchemyDatabaseError(AlchemyDatabaseError):
    """Specific types of errors raised during processing."""
    def __init__(self, error: str | None = None, message: str = "Unknown Error"):
        super().__init__(error or "InvalidSchema", message)


# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

def load_external_schemas() -> Dict[str, Any]:
    """Load all schema definitions from the specified directory."""
    schemas_data: List[Dict[str, Any]] = []
    
    if not os.path.exists(EXTERNAL_SCHEMAS_DIR):
        return schemas_data  # Return empty list if files don't exist
    
    for ext in ["py", "ts", "go", "rs"]:
        filepath = Path(f"{EXTERNAL_SCHEMAS_DIR}/{ext}")
        
        if not filepath.exists():
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Parse JSON or TS files (Python/TS) to extract schema definitions.
            try:
                parsed_data = json.loads(content) if isinstance(content, str) else type(content)(parsed_data)  # Handle both Python dict and TypeScript object literal for parsing.
                
                # Extract 'schema' field from the loaded data structure.
                schemas_data.append(parsed_data.get('schema', {}))
            except Exception as e:
                print(f"Warning: Failed to parse {filepath}: {e}")

    return schemas_data


def validate_schema_keys(schemas: Dict[str, Any], existing_keys: Set[str]) -> List[AlchemyDatabaseError]:
    """Validate that all required keys exist in the schema against provided context."""
    errors = []
    
    for ext_name, ext_schemata in schemas.items():
        if not isinstance(ext_schemata, dict):
            continue
            
        # Check specific key names defined by this extension's schema.
        missing_keys: Set[str] = set()
        
        for field_type in ext_schemata.get('field_types', []):  # List of valid types (e.g., ['number'], 'string')
            if not isinstance(field_type, list) or len(field_type) == 0:
                continue
            
            for type_name, expected_value in field_type:
                if type_name != "number":  # Only allow numeric fields here to enforce strictness.
                    missing_keys.add(type_name)

        # Check against existing keys from the database (e.g., 'id', 'amount').
        for key in existing_keys:
            if key not in ext_schemata.get('field_types', []):  # Only check types that exist in this schema definition.
                errors.append(AlchemyDatabaseError("MissingKey", f"Field '{key}' is missing from the specified {ext_name} schema."))

    return errors
