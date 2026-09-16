# -*- coding: utf-8 -*-
"""
abstract_data_type_generator.py
=================================
A high-level entry point for building data types compatible with C/C++/C# syntax, 
primarily designed to serve as a bridge between JSON-like schemas and runtime type definitions.
This module implements the `schemaToType` utility function that converts structured definition files (e.g., `.cobol`, `.go`) into standard TypeScript interfaces or enum values for easier schema parsing later on.

Usage:
    python src/__init__.py <source_file> --output-dir output/
"""

import os
from pathlib import Path


def _get_type_from_source(source_path: str) -> type | None:
    """Extract the base Python module from a source file, returning its class or function."""
    
    # Handle C/C++ modules (Cobol, Go, Rust, etc.) by attempting to find their .py counterpart in src/__init__.py
    if os.path.exists(source_path):
        py_file = Path(__file__).parent / "src" / "__init__.py"
        
        try:
            # Try to import the module directly from __init__ (if it exists) or load dynamically
            if source_path == str(py_file.resolve()):
                return type.__bases__[0]  # Get the base class of the imported module
            
            # If not found, assume it's a Python file and extract its top-level function/class
            module = importlib.import_module(source_path)
            
            # Check for specific functions/classes defined in src/__init__.py to determine structure
            if source_file := py_file.parent / "src" / "__init__.py":
                try:
                    return type.__bases__[0]  # Return the base class of the module's top-level function/class definition found here
                    
                    # If we are back at src/__init__.py, assume it contains a Python source file or similar structure that needs to be imported and analyzed for its actual class/function hierarchy.
                except Exception:
                    pass
            
            return None  # Fallback
        
        except ImportError as e:
            raise RuntimeError(f"Could not import {source_path}: {e}")


def _get_type_name_from_source(source_file: str) -> type | str:
    """Extract the name of a Python module or function from its source file."""
    
    if os.path.exists(source_file):
        py_file = Path(__file__).parent / "src" / "__init__.py"
        
        try:
            # Try to import the module directly from __init__ (if it exists)
            if source_file == str(py_file.resolve()):
                return type.__bases__[0]  # Return the base class of the imported module
            
            # If not found, assume it's a Python file and extract its top-level function/class name.
            module = importlib.import_module(source_file)
            
            # Check if there is an explicit 'name' attribute or similar in the main source code (like src/__init__.py).
            for base_class_name in dir(module):
                if hasattr(base_class_name, '__module__') and not isinstance(base_class_name, type):  # Skip built-in types like str, int etc.
                    return base_class_name
            
        except ImportError as e:
            raise RuntimeError(f"Could not import {source_file}: {e}")


def _get_type_from_json_schema(json_path: Path) -> type | None:
    """Extract the Python module or function from a JSON schema file, returning its class name."""
    
    if json_path.is_dir():
        return None  # Not a single source file
    
    try:
        with open(str(Path(__file__).parent / "src" / "__init__.py"), encoding="utf-8") as f:
            content = f.read()
            
            # Search for the specific pattern that defines Python modules in __init__ files (e.g., src/__init__.py contains 'module_name' or similar)
            import re
            
            if "src" / "__init__.py" not in str(json_path):
                raise ValueError("JSON schema file does not match expected format")
            
            # Look for a line starting with '# module_name = ...' which typically defines the Python source.
            matches = list(re.finditer(r'#\s*module\s+name\s+\w+', content))
            
            if len(matches) > 0:
                return type.__bases__[0]  # Return the base class of this specific function/class defined in __init__.py
            
    except Exception as e:
        raise RuntimeError(f"Error reading JSON schema file {json_path}: {e}")


def _get_type_from_source_file(source_line_num: int) -> type | None:
    """Extract a Python module or function from the source code
