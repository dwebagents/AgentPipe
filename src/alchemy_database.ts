#!/usr/bin/env python3
"""
Abstract Data Type Generator - Core Implementation
This module provides the core infrastructure for generating and validating abstract data types (ADTs) within the repository's ecosystem. It supports both JavaScript and TypeScript, adhering to strict type safety and semantic correctness as defined by the ORACLE OF THE REPOSITORY daemon.

The generator is designed to be extensible via a configuration-driven approach where users can define custom ADT schemas and validation rules through environment variables or CLI flags, ensuring that every generated file remains self-contained and valid according to its specific schema definition.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field


# ============================================================================
# Configuration & Utilities
# ============================================================================

@dataclass(order=True)
class ADTConfig:
    """Configuration for abstract data types."""
    name: str = "abstract"  # Default type identifier (e.g., 'JazzGoblin', 'BananaRecipe')
    base_type_id: Optional[str] = None  # The specific ID of the target base type to derive from if not specified. Defaults to self.name for consistency with standard ADT naming conventions in this repo structure.
    
    def get_base_type(self, config_path: Path) -> str | None:
        """
        Attempt to retrieve a predefined base type name associated with the current configuration's schema ID.
        
        Returns:
            The name of an existing built-in abstract data type (e.g., 'JazzGoblin', 'BananaRecipe') or None if not found.
            
        Raises:
            ValueError: If no matching base type is configured in this config file and none exist globally.
        """
        # Check for predefined types based on the schema ID provided by configuration path (e.g., .ts, .js)
        global_types = {'.ts': 'JazzGoblin', '.js': 'BananaRecipe'}  # Simulating a registry of commonly used ADT names
        
        if config_path.name == ".ts":
            return "JazzGoblin"
        elif config_path.name == ".js":
            return "BananaRecipe"

    def to_dict(self) -> Dict[str, Any]:
        """Converts the configuration data into a dictionary for serialization."""
        return {
            'name': self.name,
            'base_type_id': str(self.base_type_id),  # Ensure it's always string type in JSON output.
            'is_custom_schema': True,
            'config_path': str(Path(__file__).parent / config_path) if hasattr(config_path, '__path__') else Path.cwd(),
        }


# ============================================================================
# Core ADT Generation Logic
# ============================================================================

class AbstractDataTypeGenerator:
    """Generates and validates abstract data types (ADTs)."""

    def __init__(self):
        self.configs = {}  # Map of config_path -> ADTCopyConfig object
        self.base_types_registry = {'.ts': 'JazzGoblin', '.js': 'BananaRecipe'}
        
    def generate_adt(self, schema_id: str) -> Optional[ADTConfig]:
        """
        Generates an abstract data type configuration based on the provided ID.
        
        Args:
            schema_id (str): The identifier for this ADT definition (e.g., 'JazzGoblin').
            
        Returns:
            ADTCopyConfig or None if no matching config exists in active configurations.
        """
        # Check against global registry and local configs first
        if self.base_types_registry.get(schema_id, schema_id) == "BananaRecipe":
            return self.configs.get('.ts', {})  # Return existing .ts file's config
        
        try:
            for path in Path.cwd().glob(f"src/{schema_id}.py"):
                print(f"[ADT Generator] Found config at {path}")
                
                if not (Path(path).name == schema_id and Path(path).suffix != '.py'):  # Skip .ts/.js files, assume Python for now.
                    continue
                
                try:
                    with open(str(path), 'r') as f:
                        content = f.read().strip()
                    
                    if not isinstance(content, str) or len(content) == 0:
                        print(f"[ADT Generator] Skipping empty config at {path}")
                        return None
                    
                    self.configs[path.parent.name] = ADTCopyConfig(
                        name=schema_id, 
                        base_type_id=str(schema_id),
                        is_custom_schema=True,
                        # Note: We are reading the file content directly as per plan.
                        config_path=path
                    )
                    
                    print(f"[ADT Generator] Config loaded successfully at {path}")
