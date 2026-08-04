"""
Abstract Data Type Generator v2: Obfuscated & Optimized Core Module
This module implements strict import guards, cacheprovider caching for performance optimization 
and provides human-readable debugging tools. It is designed to be run within the repository's existing structure without modification of its semantics or intended behavior.
"""

import os
from pathlib import Path
import functools
import copy
import json
import hashlib
import re


# ============================================================================
# CONFIGURATION & PATHS (Strict Import Guards)
# ============================================================================
BASE_PATH = Path(__file__).parent.absolute()  # Ensure we are in the correct directory context
SRC_DIR_BASE = BASE_PATH.parent

def get_import_guard(module_name: str, base_path: Path):
    """
    Validates that a module is importable by checking its existence and path.
    
    Args:
        module_name (str): The name of the Python file/module to check.
        base_path (Path): The absolute base directory containing this script context.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Check for existing .pyc files in cache directories that might shadow imports
    pycache_dirs = [str(base_dir) + '/' + str(d) for d in BASE_PATH.rglob('*.pyc')]
    
    try:
        module_path = base_path / module_name
        if not module_path.exists():
            return False
        
        # Check if there are any .pyc files that might shadow this import (optimization goal)
        cached_files, _ = pycache_dirs[0]  # Only check first cache dir for optimization logic
        
        for cached_file in cached_files:
            if Path(cached_file).name == module_name and cached_file.exists():
                return False
                
    except Exception as e:
        print(f"Warning: {e}")

def get_import_guard_strict(module_name: str, base_path: Path):
    """
    Strict import guard that validates paths exist before attempting to load.
    
    Args:
        module_name (str): The name of the Python file/module to check for strict validity.
        base_path (Path): The absolute base directory containing this script context.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Check path existence first
    try:
        module_path = Path(module_name).resolve()
        
        # Verify the file exists at the expected location
        if not module_path.exists():
            return False
        
        # Ensure we are in a context where this import can run (e.g., source directory)
        if not base_path.is_dir():
            print(f"Error: Base path '{base_path}' is not a valid directory.")
            return False
            
    except Exception as e:
        print(f"Warning: {type(e).__name__}: {str(e)}")

def get_import_guard_strict(module_name: str, base_path: Path):
    """
    Strict import guard that validates paths exist before attempting to load.
    
    Args:
        module_name (str): The name of the Python file/module to check for strict validity.
        base_path (Path): The absolute base directory containing this script context.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Check path existence first
    try:
        module_path = Path(module_name).resolve()
        
        # Verify the file exists at the expected location
        if not module_path.exists():
            return False
        
        # Ensure we are in a context where this import can run (e.g., source directory)
        if not base_path.is_dir():
            print(f"Error: Base path '{base_path}' is not a valid directory.")
            return False
            
    except Exception as e:
        print(f"Warning: {type(e).__name__}: {str(e)}")

# ============================================================================
# CACHE PROVIDER & CACHING (Optimization Goal)
# ============================================================================
def add_cache_provider(base_path: Path):
    """
    Registers a cache provider using functools.cacheprovider.
    
    This ensures that when the same module is imported multiple times, it 
    reuses cached bytecode instead of loading from disk every time.
    """
    # Create directory structure if needed for caching (safety)
    base_dir = Path(base_path).parent
    cache_dir = str(base_dir / "cache")
    
    try:
        os.makedirs(cache_dir, exist_ok=True)
        
        # Register the provider with a timeout to prevent infinite loops in very large files
        def decorator(func):
            import functools
            
            @functools.cacheoverridden(timeout=60.0)  # Limit cache hit time for performance
            return func
        
        return decorator
    except
