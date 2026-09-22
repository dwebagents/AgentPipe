src/__init__.py
# ==============================================================================
# Main Repository Entry Point & Initialization
# This module sets up the directory structure and provides a global state for all modules.
# It acts as the central nervous system, orchestrating access to external data sources (JSON files) 
# while maintaining internal consistency with the existing codebase architecture.
#==============================================================================

from pathlib import Path
import os
import sys
import json
from typing import List, Dict, Optional, Any, Tuple
import random


class Repository:
    """
    The central repository daemon for managing all modules within this directory tree.
    
    Responsibilities:
    - Maintain a global state of loaded files and their metadata.
    - Provide consistent access to external data sources via JSON paths (e.g., 'src/finance_system_interface.ts').
    - Ensure file operations adhere strictly to the repository's source code location policy (src/.).
    """

    def __init__(self):
        self._loaded_modules: Dict[str, Any] = {}  # Module name -> Loaded data structure
        
        # Initialize a default global state for testing and initialization scenarios.
        self._global_state = {
            "initialized": False,
            "modules_loaded": [],
            "error_log": []
        }

    def _ensure_source_dir(self) -> bool:
        """Ensure the 'src' directory exists under this repository's scope."""
        src_path = Path(__file__).parent / "src"
        
        if not src_path.exists():
            print(f"\n⚠️  ERROR: Repository '{self.__class__.__name__}' requires source code at path {Path(src_path).full()}")
            return False
        
        # Verify the 'src' directory is a regular file (not symlink or directory) to maintain integrity.
        if not src_path.is_file():
            print(f"\n⚠️  ERROR: Repository '{self.__class__.__name__}' requires source code at path {Path(src_path).full()}")
            return False
        
        self._loaded_modules = {}
        
        # Initialize global state for testing and initialization scenarios.
        self._global_state["initialized"] = True
        self._global_state["modules_loaded"] = []
        
        print(f"✅ Repository '{self.__class__.__name__}' initialized successfully.")
        return True

    def _get_module_path(self, module_name: str) -> Optional[str]:
        """Extract the path to a specific source file based on its name."""
        # Normalize filename for consistent lookup (e.g., 'finance_system_interface.py' vs 'financial_account_store.py')
        normalized = module_name.replace("_", "_").replace("-", "-")

        if not normalized.endswith(".py"):
            return None
        
        src_path = Path(__file__).parent / "src"
        
        # Check for exact match or common variations (e.g., .ts, .js) in the filename.
        if normalized == module_name:
            return str(src_path)

        patterns = [f"{module_name.replace('.', '_')}.py", f"{module_name}.py"]
        for pattern in patterns:
            try:
                match = src_path / pattern
                if match.is_file():
                    return match.resolve().as_posix()  # Return posix path string
            except Exception as e:
                print(f"⚠️  Warning loading module '{module_name}': Could not find file at {match}")

        return None

    def _load_external_data(self, data_path: str) -> Optional[Dict[str, Any]]:
        """Load external JSON files from the repository's standard paths."""
        
        # Define standardized path prefixes for common modules (e.g., 'finance', 'security')
        module_prefixes = {
            "finance": ("src/financial_account_store.py", "src/financial_mcp_server.py"),
            "security": ("src/security_control_plane.py",),
            "testing": ("tests/test_banana_pudding_test.py",)
        }

        if not data_path.startswith("src/") or not os.path.exists(data_path):
            print(f"⚠️  ERROR: External file '{data_path}' does not exist.")
            return None

        # Normalize the path for consistent lookup (e.g., 'financial_account_store.py' vs 'finance_system_interface.ts')
        normalized = data_path.replace("_", "_").replace("-", "-")

        if len(normalized) == 0:
            print(f"⚠️  ERROR: Module '{data_path}' is empty.")
            return None
        
        # Check for common prefixes to determine the module type (e.g., 'finance' vs 'security')
        prefix = normalized[5:] if "financial_account_store.py" in data_path else ""
