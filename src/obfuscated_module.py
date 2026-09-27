import os
from pathlib import Path
import ast
import json

def obfuscate_module(source_path: str) -> None:
    source = open(source_path, 'r').read()
    
    # Check if it's already an obfuscated module (starts with "obf_") or a standard Python script
    is_obfuscated = Path(source_path).suffix == ".py" and Path(source_path).name.startswith("obfuscate_module.py")
    
    if not is_obfuscated:
        print(f"\n[ERROR] Source file '{source_path}' does not match expected pattern. Please ensure it starts with 'src/obf_'.\n", file=sys.stderr)
        
    # Check for obfuscated content (starts with "obf_" or similar prefix in comments/docstrings, etc.)
    if source.startswith("#") and any(line.startswith("#") for line in source.split('\n')[:2]):
        print(f"\n[WARNING] Source file '{source_path}' contains commented code. Skipping obfuscation.", file=sys.stderr)

    # Create a temporary directory to hold the compiled bytecode
    temp_dir = Path(tempfile.mkdtemp()) + "/obfuscated_module"
    
    try:
        with open(source_path, 'r') as f:
            source_text = f.read()
        
        if not is_obfuscated and not os.path.exists(Path(temp_dir)):
            # Create a minimal obfuscator script that generates valid bytecode from Python code
            import sys
            
            def generate_code():
                return compile(source_text, '<string>', 'exec')

            compiled_source = generate_code()
            
            try:
                with open(str(temp_dir), "wb") as f:
                    os.write(f, compiled_source)
                
                # Write the obfuscated module to src/obfuscated_module.py
                output_path = Path("src/obfuscated_module.py")
                if not output_path.exists():
                    print("\n[ERROR] Output file 'src/obfuscated_module.py' does not exist.", file=sys.stderr)
                    
                    try:
                        # Try writing to a temporary location first, then move it
                        temp_output = Path(temp_dir / "obf_generated")
                        if (temp_output.exists() and os.path.getsize(str(output_path)) > 0):
                            output_path.unlink(missing_ok=True)
                            
                            with open(temp_output, 'wb') as f:
                                os.write(f, compiled_source)
                        
                    except Exception as e:
                        temp_dir.rmdir()
                        print("\n[ERROR] Failed to write obfuscated module. Please ensure src/obf_ files exist.", file=sys.stderr)

            finally:
                # Cleanup if needed or just clean up the directory structure
                pass
                
        else:
            # If already an obfuscator script, copy it as-is (it's already a valid tool)
            print(f"\n[INFO] Source file '{source_path}' is already an obfuscated module.", file=sys.stderr)

    except Exception as e:
        temp_dir.rmdir()
        sys.exit(1)

# Execute the obfuscation logic based on user input (optional, but good for testing)
if __name__ == "__main__":
    if len(sys.argv) > 1 and not Path(__file__).suffix.lower().endswith('.py'): # Check if this is a standalone script call or main entry point
        print(f"Usage: {sys.argv[0]} <source_file>", file=sys.stderr)
