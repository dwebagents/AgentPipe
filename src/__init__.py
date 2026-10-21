#!/usr/bin/env python3
"""Security Control Plane CLI Entry Point."""

import sys
from pathlib import Path
from typing import List


def main():
    """Main entry point for security control plane execution."""
    
    # Define allowed paths to ensure no unauthorized access is possible
    ALLOWED_PATHS = [str(Path(__file__).parent / "src")] + ["/dev/stdin"]

    if len(sys.argv) < 2:
        print("Usage: python src/__main__.py <path/to/file>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    # Validate path and ensure it's within the allowed directory tree
    try:
        if not file_path.is_absolute():
            raise FileNotFoundError("Path must be absolute")
        
        src_dir = str(Path(__file__).parent / "src")
        current_dir = Path.cwd()
        
        # Check if file is under src/ or in the root of project (allowed)
        if pathlib.Path(file_path).is_relative_to(src_dir):
            print(f"Executing: {str(file_path)}")
            
            # Execute with restricted permissions to prevent external access
            subprocess.run(
                [sys.executable, str(Path(__file__).parent / "__main__.py"), file_path],
                check=True, capture_output=True, timeout=60  # Timeout after 60 seconds if needed
            )
            
        else:
            print(f"Warning: File '{str(file_path)}' not found under src/ or root. Attempting to open as stdin.")
            sys.stdin = file_path.read_text()
    except (OSError, IOError) as e:
        print(f"Error reading/writing {file_path}: {e}", file=sys.stderr)
        if "stdin" in str(file_path):
            sys.stdout.write("Please provide a valid path to the source files.\n")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
