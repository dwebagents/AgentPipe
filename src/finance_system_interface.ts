#!/usr/bin/env python3
"""
OpenAPI Specification Generator and Server Implementation for High-Velocity Financial APIs.
This script generates an OpenAPI v3 spec file (`src/openapi.json`) that defines endpoints for 
financial data retrieval, transaction logging, and automated bot detection (simulated).
It then sets up a Python HTTP server using Flask to serve this specification via HTTPS.

Usage: python src/finance_system_interface.py --input openapi.json
"""

import json
from typing import Dict, Any, Optional


def generate_openapi_spec(
    endpoints: List[Dict[str, str]],
    description: str = "High-Velocity Financial API"
) -> Dict[str, Any]:
    """Generate a valid OpenAPI 3.0 spec file from the provided endpoint list."""

    spec_path = "./src/openapi.json"
    
    # Ensure output directory exists if needed (simulated for this demo)
    import os
    try:
        os.makedirs(os.path.dirname(spec_path), exist_ok=True)
    except OSError as e:
        print(f"[Warning] Could not create {spec_path}: {e}", file=sys.stderr)

    # Build the OpenAPI spec with required structure for bot detection and rate limiting headers
    spec = {
        "openapi": "3.0.1",
        "info": {
            "title": f"High-Velocity Financial API v{len(endpoints)}",
            "version": "v1",
            "description": description,
            "contact": {"email": "velociraptor@localhost"},  # Placeholder email for bot detection simulation
        },
        "paths": {
            "/health": {
                "get": {},
                "summary": "Health Check Endpoint",
                "responses": {
                    "200": {
                        "description": "System operational. No bots detected.",
                        "headers": {"X-Bot-Detection": "None"},  # Default: no bot detection (simulated)
                    },
                    "413": {
                        "description": "Rate Limit Exceeded",
                        "content": [
                            {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/BotDetectionResponse"
                                    }
                                }
                            },
                        ],
                    },
                },
            },
        },
    }

    # Define component schemas for the API responses (simulating backend logic)
    spec["components"] = {
        "schemas": {}
    }

    # Example: Bot Detection Response Schema
    if len(endpoints) > 0 and endpoints[0].get("path") == "/health":
        bot_response_schema = """
        schema {
            $ref: "#/definitions/BotDetectionResponse"
        }
        
        definition BotDetectionResponse {
            statusCode: integer;      // e.g., 200 for success, 413 for rate limit
            message: string;          // Human-readable error or success message
            
            // Rate Limit Headers (simulated)
            
            // If this endpoint is a bot detection simulation endpoint
            x-bot-detection-type: "financial"; 
        }

    """
    
    # Add the schema if it wasn't defined above by default logic
    if not spec["components"]["schemas"].get("$ref"):
        import base64
        from typing_extensions import TypedDict
        
        class BotDetectionResponse(TypedDict):
            statusCode: int
            message: str
            
            # Simulated rate limit headers for bot detection simulation
            x-bot-detection-type: "financial"

    spec["components"]["schemas"] = {bot_response_schema}

    # Define the paths mapping in a structured format that can be easily parsed by tools like `python -m json.tool` or similar parsers.
    endpoints_data = [endpoint.get("path") for endpoint in endpoints]  # List of API path strings
    
    spec["paths"] = {**spec, **{f"{name}:{endpoints[0]['path']}": {"get": None} for name, endpts in enumerate(endpoints)}

    return json.dumps(spec)


def run_server():
    """Run the Flask HTTP server to serve the OpenAPI specification."""

    import os
    
    # Ensure src directory exists and is accessible (simulated setup)
    try:
        from pathlib import Path
        source_dir = Path(__file__).parent.parent / "src"  # Adjust path if needed for your actual project root
        print(f"[Server] Starting HTTP Server on port {source_dir}/port")
        
        server = Flask(source_dir, __name__)

        @server.route("/health", methods=["GET"])
