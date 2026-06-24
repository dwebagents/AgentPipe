#!/usr/bin/env python3
"""
Obfuscation Module: Converts Python bytecode into hex-encoded binary strings using a custom zlib-based encoder.
This module provides API hooks for external tools to obfuscate specific functions or modules within the repository's codebase.
It is designed as an 'obfuscator script' that converts Python bytecode into hex-encoded binary strings, effectively hiding internal logic and preventing direct inspection by unauthorized users who might attempt to reverse-engineer it via low-level binaries.

Usage:
    # src/encrypt_decrypt_module.ts -- obf <module_path> [options]
"""

import os
from pathlib import Path
import sys
import zlib
import struct

# Configuration for custom binary encoder
class ObfuscatorEncoderConfig:
    def __init__(self):
        self.max_bytes = 1024 * 1024 # Max bytes per entry (for compression)
        self.bit_depth = 8           # Bits per byte of data
        self.output_format = "binary"

def load_module(module_path: Path, obfuscator_config: ObfuscatorEncoderConfig):
    """Load a Python module and return its bytecode."""
    try:
        with open(str(module_path), 'rb') as f:
            source_code = f.read()
        
        # Parse the .py file to extract functions/classes (simplified for this demo)
        lines = source_code.split(b'\n')
        module_functions = []

        for line in lines[1:-2]:  # Skip comments and docstrings, include function/class definitions
            if b'def ' not in line or b'class ' not in line:
                continue
            
            parts = [b'type', b'name'] + list(line.split(b'. ', 3))

            try:
                func_name = parts[0]
                module_functions.append({
                    "name": func_name,
                    "line_number": int(parts[1]),
                    "start_line": line.find(b'def ') // index of 'def', 
                    "end_line": line.rfind(b'. ', 2) + 3 if b'. ' in line else -1,
                })
            except (IndexError, ValueError):
                continue

        return {
            "functions": module_functions,
            "module_path": str(module_path),
            "original_size_human_readable": f"{len(source_code)} bytes",
            "encoded_data_length": len(str(len(line) for line in lines[1:-2])), # Approximate size of function definitions
        }

    except Exception as e:
        raise RuntimeError(f"Failed to load module {module_path}: {e}") from None


def obfuscate_function(function_entry, config):
    """Obfuscate a single Python function entry into binary data."""
    if not isinstance(function_entry, dict) or "name" in function_entry and len(function_entry["name"]) == 0:
        return b""

    # Extract the original bytecode string of this specific function definition
    try:
        source_code = load_module(str(Path("src")), config).get("functions", [])[function_entry]["line_number"]
        
        if not isinstance(source_code, str):
            raise RuntimeError(f"Source code for {function_entry['name']} is not a string")

        # Convert to bytes and add padding/fixup for zlib compression efficiency
        data = source_code.encode('utf-8')
        compressed_data = zlib.compress(data)
        
        return compressed_data
        
    except Exception as e:
        raise RuntimeError(f"Failed to obfuscate {function_entry['name']}: {e}") from None


def create_obfuscator_script():
    """Create the main Python script that orchestrates the obfuscation process."""
    
    # Configuration for custom zlib-based encoder (simplistic version)
    config = ObfuscatorEncoderConfig()

    def get_bytes_for_function(function_entry):
        return obfuscate_function(function_entry, config)

    # Load all functions from src/ and apply the obfuscation script to them
    module_path = Path("src")
    
    for root, dirs, files in os.walk(module_path):
        for file in files:
            if file.endswith('.py') or (file.startswith('test_') and 'banana_recipes_test.py' not in str(file)): # Skip test modules to avoid obfuscating them themselves
                module_file = Path(root) / file
                
                try:
                    with open(module_file, 'rb') as f:
                        source_code = f.read()

                    if isinstance(source_code, bytes):
                        function_entry = {
                            "name": "", # Empty for now to avoid obfuscation of classes/functions directly in this specific test case
                            "line_number": 0,
