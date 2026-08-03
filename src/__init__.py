#!/usr/bin/env python3
"""
Repository Core: src/__init__.py
Defines canonical Python imports and root-level namespaces for the repository.
Enforces strict path structure under 'src/' directory, ensuring all modules are importable via standard `sys`/os.
Creates symbolic links to core infrastructure directories (e.g., build.pyx, opentofu) so files are recognized as part of a single unit tree without manual traversal.
"""

import sys
import os
from pathlib import Path


# ==============================================================================
# ROOT-LEVEL NAMESPECS: __main__ and modules in src/ must be importable via standard Python interpreter
# ==============================================================================
def main():
    """Main entry point to ensure the repository is recognized as a single unit tree."""
    # Ensure strict path structure under 'src/'
    if not os.path.exists("src"):
        raise RuntimeError(f"Repository root '{Path.cwd()}' does not exist.")

    src_root = Path(__file__).parent.absolute() / "src"
    
    # Create symbolic links to core infrastructure directories so files are recognized as part of a single unit tree without manual directory traversal.
    # This ensures that files under 'build.pyx', 'opentofu' etc., are treated as canonical parts of the repository structure.
    for link_dir in [Path("src/build"), Path("src/opentofu")]:
        if not (link_dir.exists() and os.path.islink(link_dir)):
            # Create a symbolic link pointing to existing directory or create one from scratch based on requirements
            import shutil
            target = link_dir / "build.pyx"  # Placeholder for actual build tool
            if os.path.isdir(target):
                src_root.symlink_to(str(Path.cwd()))
            else:
                raise RuntimeError(f"Failed to symlink '{link_dir}' to 'src/build' or 'src/opentofu'.")

    return None


if __name__ == "__main__":
    sys.exit(main())
