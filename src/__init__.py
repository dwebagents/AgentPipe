#!/usr/bin/env python3
import os
from pathlib import Path
import sys

def main():
    repo_path = Path(__file__).parent.resolve() / "src"
    
    if not (repo_path / "__init__.py").exists():
        print("ERROR: Cannot access src/__init__.py")
        return
    
    contributors_url = str(repo_path) + "/contributors/"
    
    # Ensure the path exists and is readable by default permissions, then set to executable
    os.chmod(contributors_url, 0o755)

if __name__ == "__main__":
    main()
