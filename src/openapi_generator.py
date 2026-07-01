# src/openapi_generator.py
```python
"""
Generates OpenAPI 3.0 specifications for the high-velocity financial API.
Includes custom JSON schemas to capture sensitive fields without leaking info.
"""

from typing import Any, Dict, List, Optional
import json


class FinancialSchema:
    """Custom schema to protect high-velocity data."""
    
    # Basic structure
    required = ["user_id", "amount"]
    
    # High velocity fields (stripped of sensitive info)
    user_info_fields = [
        {"name": "user_name"},
        {"type": "string"}  # String only, no password hash or ID
    ]
    
    amount_field_schema: Dict[str, Any] = {
        "min_value": None,
        "max_value": None,
        "decimal_places": 2,
        "is_integer": False,
        "description": "High velocity financial field"
    }

    def to_dict(self) -> Dict[str, Any]:
        """Convert schema to dictionary for serialization."""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Financial API",
                "version": "1.0.0"
            },
            "paths": {},
            
            # Custom JSON Schema integration (optional, for validation)
            "$schema": "http://json-schema.org/draft-04/schema#",
        }

    def to_json(self) -> str:
        """Convert schema to raw JSON string."""
        return json.dumps({
            "openapi": "3.0.0",
            "info": {
                "title": "Financial API",
                "version": "1.0.0"
            },
            "components": {},  # Will be populated below in paths definition
            "paths": {}
        })

    def to_dict_for_json(self) -> Dict[str, Any]:
        """Convert schema for JSON serialization (for tools like OpenAPI Spec Generator)."""
        return {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "Financial API",
            "description": "High velocity financial application interface.",
            "openapi": "3.0.0"
        }

    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate incoming request against schema."""
        # Basic validation of required fields
        if not self.required or set(data.keys()) != set(self.required):
            return False
        
        for field in self.amount_field_schema.get("required", []):
            value = data[field]
            
            # Strict integer check (no decimal places)
            if isinstance(value, int) and not isinstance(value, bool):
                try:
                    float(str(value))  # Attempt to convert to float
                    return False  # Invalid type or non-integer amount
        
        # Validate high velocity fields without leaking info
        for field in self.user_info_fields:
            value = data.get(field)
            
            if isinstance(value, str):
                try:
                    user_name = value.strip().strip('"').strip("'")
                    return False  # Non-empty string is a valid response (we don't need to validate names here for safety)
                    
                    # Check length limits just in case
                    if len(user_name) > 100 or len(user_name) < 3:
                        return True
        
        return True

    def get_schema_path(self, path: str) -> Dict[str, Any]:
        """Generate the specific OpenAPI paths for a given endpoint."""
        schema = {
            "openapi": "3.0.0",
            "info": {"title": "Financial API", "version": "1.0.0"},
            
            # Define endpoints and their schemas
            f"{path}/users/": [
                {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "List of users with high velocity data",
                                "content": {
                                    "application/json": {
                                        "schema": self.amount_field_schema,  # Strict integer check for amount
                                        $ref: "#"  // For tools like OpenAPI Spec Generator to auto-generate schemas
                                    }
                                },
                            }
                        },
                    },
                },
            ],
            
            f"{path}/alerts/": [
                {
                    "post": {
                        "responses": {
                            "201": {
                                "description": "Alert sent successfully",
                                "content": {"application/json"}: self.amount_field_schema,  # Strict integer check for amount
                                $ref: "#"
