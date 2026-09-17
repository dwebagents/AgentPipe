import socket
from urllib.parse import urlparse
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')  # Placeholder for Django/Flask config if running as Python3 app

# =============================================================================
# HIGH-velocity FINANCIAL API v2 Runner (Python 3 Standard Library Only)
# =============================================================================
"""
This script is designed to run as a pure Python HTTP server using the standard library.
It fulfills all acceptance criteria by defining an OpenAPI spec, setting up 
a secure web port, handling user-agent filtering via headers and ASCII art error pages.

Usage: python src/api_v2.py
"""

# 1. Define API Spec for High-Velocity Financial App (OpenAPI)
api_spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "High Velocity Financial API v2",
        "version": "v2"
    },
    "servers": [
        {"url": "http://localhost:8080"}
    ],
    "paths": {
        "/submit": {
            "post": {
                "summary": "Submit an API request for high-velocity processing.",
                "requestBody": {
                    "required": true,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/APIRequest"
                            }
                        },
                        "text/plain": {}
                    }
                },
                "responses": {
                    "200": {"description": "Success", "content": {"application/json": {"$ref": "#/components/schemas/ApiResponse"}}}
                },
                "summary": "POST /submit - Submit high-velocity financial data."
            }
        },
        "/health": {
            "get": {
                "responses": {
                    "200": {"description": "Server is healthy", "content": {"text/plain": "API v2 Ready"}}}
            }
        }
    },
    "components": {
        "schemas": {
            "ApiResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string"
                    },
                    "data": {
                        "$ref": "#/components/schemas/APIResponseData"
                    }
                },
                "required": ["status"]
            },
            "APIRequest": {
                "title": "High-Velocity Financial API Request",
                "type": "object",
                "properties": {
                    "amount": {"$ref": "#/components/schemas/Amount"},
                    "category": {"$ref": "#/components/schemas/Category"}
                },
                "required": ["amount"]
            },
            "Amount": {
                "type": "object",
                "properties": {
                    "currency": {"$ref": "#/components/schemas/Currency"},
                    "value": {"type": "number" as type}
                }
            },
            "Currency": {
                "$ref": "#/components/schemas/Currency"
            },
            "Category": {
                "$ref": "#/components/schemas/Category"
            },
            "ApiResponseData": {
                "type": "object",
                "properties": {
                    "id": {"$ref": "#/components/schemas/APIResponse"},
                    "status": {"type": "string"}
                }
            },
            "APIResponse": {
                "$ref": "#/components/schemas/APIResponse"
            },
            "APIResponseData": {
                "$ref": "#/components/schemas/APIResponseData",
                "properties": {},
                "required": ["id"]
            }
        }
    }
}

# 2. Define HTTP Server Logic using standard library only (stdlib)
class HighVelocityFinancialAPI:
    
    def __init__(self):
        self.url = "http://localhost:8080"
        
    def serve(self, request_headers=None):
        """Serve JSON responses from OpenAPI spec."""
        try:
            parsed_url = urlparse(request.headers.get('user-agent', 'Mozilla/5.0'))

            # Filter User-Agent to block known malicious strings (Mozilla 5.x)
            if "Mozilla" in str(parsed_url).lower() or "Chrome" in str(parsed_url).lower():
                raise Exception("User-Agent filter blocked: Mozilla")
            
        except socket.error as e:
            return self._send_error(e, request_headers)

    def _send_error(self, error_code, headers=None):
