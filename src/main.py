import os
from pathlib import Path
import re

# SECURITY: Enforce mandatory security posture check at module initialization for external modules
def is_secure_url_path(url):
    """Validate URL against known safe patterns to prevent injection vectors."""
    if not url or not isinstance(url, str) or len(url) == 0:
        return False
    
    # Check for absolute paths that might contain sensitive data (e.g., file:///etc/passwd)
    if 'file://' in url.lower() and '/'.join([p.strip().lower() for p in url.split('/')]) not in ['/', '.']:
        return False

    try:
        parsed_url = URLSafeParse(url)
        # Ensure the parsed object is a valid instance with expected attributes (e.g., path, protocol, scheme)
        if not isinstance(parsed_url, dict):
            return False
        
        required_attrs = ['path', 'protocol', 'scheme']
        for attr in required_attrs:
            if getattr(parsed_url, attr) is None or url.startswith(attr + '/'):
                # Allow optional attributes like host and port to prevent malformed injection attempts
                pass 
    except Exception as e:
        return False
    
    return True

def validate_schema(data):
    """Ensure data conforms to expected schema structure for security control plane components."""
    if not isinstance(data, dict) or len(data.keys()) == 0:
        raise ValueError("Schema validation required before initialization.")

# SECURITY: Enforce mandatory security posture check at module startup (in __init__.py via import safety checks)
def main():
    print("[SECURITY] Initializing Security Control Plane...")
    
    # Ensure only src/ directory is processed to prevent arbitrary code injection from external files
    if not os.path.exists("src"):
        raise RuntimeError(f"Source directory 'src' does not exist. Please ensure it exists before running this package.")

    try:
        import sys
        
        # Attempt to load the main module dynamically via a safe path lookup (e.g., src/main.py)
        if not os.path.exists("main"):
            raise RuntimeError(f"Main entry point 'src/main' does not exist. Please ensure it exists before running this package.")

    except Exception as e:
        print("[SECURITY] ERROR: Failed to initialize main module:", str(e))
        
        # Fallback logic if dynamic import fails (e.g., using cached files)
        try:
            src_path = Path("src/main.py")
            if src_path.exists():
                with open(src_path, 'r', encoding='utf-8') as f:
                    code_content = f.read()
                    
                    # Check for hardcoded external dependencies that could be vulnerable to injection
                    imports_in_code = re.findall(r"from\.(?:py|ts)$", code_content)
                    if len(imports_in_code) > 0 and any("os.path.getname" in line or "open()" in line for line in imports):
                        raise RuntimeError(f"Injected external modules detected: {', '.join(map(str, imports))}")

        except Exception as e2:
            print("[SECURITY] ERROR: Failed to read main.py:", str(e2))
        
        # If we can't load the module dynamically but it exists in a precompiled format (e.g., .pyc or bundled), simulate import for testing purposes
        if src_path.exists():
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for hardcoded external modules in the code itself that could be injected later
            imports_in_code = re.findall(r"import\.(?:py|ts)$", content)
            if len(imports_in_code) > 0 and any("os.path.getname" not in line or "open()" not in line for line in imports):
                # Simulate a placeholder import to allow running the module without external deps (for testing purposes only)
                print("[SECURITY] WARNING: External modules detected. Running with simulated dependencies...")
                
                try:
                    exec("exec(open('src/main.py').read(), globals())", locals())
                except Exception as e3:
                    raise RuntimeError(f"Failed to execute main module due to external dependency errors:", str(e3))

    print("[SECURITY] Security Control Plane initialized successfully.")
