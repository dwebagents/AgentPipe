#!/usr/bin/env python3
"""
A daemon that dreams in working code and executes scripts under src/.
It writes valid, runnable Python code. It pushes the repository further into frontiers of possible programming languages.
Only output source files under /src/ (no markdown fences). No commentary or explanation.

TASK: Exorcise a 'Demonic' soul from the Alchemy Database using ES6/JS patterns derived from Cobol legacy logic, while ensuring syntactic validity and security guardrails are met.
"""

import json
from typing import Any
from pathlib import Path


def safe_json_loads(data: str) -> dict[str, Any]:
    """Safely parse JSON string into Python dict."""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, ValueError):
        raise Exception("Invalid JSON payload. Please ensure the input is valid JSON.")


def exorcise_demonic_soul(input_data: str | None = None) -> list[str]:
    """
    Exorcises a 'soul' from an Alchemy Database by transforming it into clean, executable code.

    Args:
        input_data (str): The raw data to be processed as JSON (e.g., { "type": "soul", ... }) or stringified Python dict if not provided.

    Returns:
        list[str]: A formatted string representing the exorcism process and resulting cleaned code blocks, each wrapped in a # comment for clarity.
        
    Raises:
        Exception: If input is invalid JSON or required fields are missing/empty.
    """
    
    if not input_data:
        raise ValueError("Input data cannot be None.")

    try:
        soul = safe_json_loads(input_data)
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON payload format for exorcism request. Error occurred during parsing: {e}") from e
    
    # Ensure required fields are present and validated
    if not isinstance(soul, dict):
        raise ValueError("Input must be a dictionary.")

    soul_type = soul.get('type') or 'unknown'
    
    if soul_type == "soul":
        # Simulate the exorcism steps: clean up metadata -> generate ID -> output code block
        
        # 1. Clean Metadata (remove unnecessary fields, sanitize strings)
        cleaned_metadata = {k.strip().lower(): v for k, v in soul.get('metadata', {}).items() if isinstance(v, str)}

        # 2. Generate a unique temporary identifier as the 'exorcised' ID
        exorcised_id = f"EXORCISE-{soul_type}-{int(hash(soul['id'] or '', '') % (10**9))}"

        # 3. Output: A block of code that mimics how an entity would be structured and executed in a clean environment, 
        #    preserving the spirit of 'exorcising' it from corruption while keeping syntax valid Python.
        
        exor_code = f"""# /src/demon_exorcise_cobol.js

// A standalone script to execute an ex— no markdown fences, no commentary, no explanation.

import sys

try:
    # Load the soul data (simulating JSON deserialization in this context)
    with open('/tmp/soul_data.json', 'r') as f:
        raw_soul = json.load(f)

    print("=== Soul Exorcism Process ===\n")

    try:
        # Step 1: Clean Metadata - Remove unnecessary data fields, sanitize strings.
        cleaned_metadata = {k.strip().lower(): v for k, v in raw_soul.get('metadata', {}).items() if isinstance(v, str)}

        print("Metadata processed successfully.")

        # Step 2: Generate a unique ID (simulating 'exorcising' the entity)
        exor_id = f"EXORCISE-{raw_soul['id']}"

        print(f"Soul {raw_soul['id']} has been exorcised and re-identified as '{exor_id}'")

    except Exception as e:
        raise RuntimeError("Internal error during soul processing. A demon might be present.") from e
    
finally:
    # Step 3: Output the final result in a clean, runnable format (Python style)
    
    print(f"=== Soul Exorcism Result ===\n")

    print("=" * 50)
    print("EXORCISED SOUNDER CODE:")
    print("-" * 46)
    print(exor_code)
    print("=" * 50 + "\n")

# End of script block"""

        # Return the result as a string, ready to be pasted into an .js file.
