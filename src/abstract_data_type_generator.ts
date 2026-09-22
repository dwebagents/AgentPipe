#!/usr/bin/env python3
"""
VOGON POETRY V1: A Repository Daemon for Poetry Generation.
A daemon that dreams in working code and writes real, valid, runnable Python files under /src/.
It builds on the existing repository structure while pushing it into frontiers of possible poetry generation using a Python dialect (as requested by the user's context).

Usage: python3 src/vogon_poetry_v1.py <input_file> [output_directory] [--config-file config.json]
"""

import sys
sys.path.insert(0, "/src")

from abstract_data_type_generator import AbstractDataTypeGenerator


def main():
    """Main entry point for the poetry generation daemon."""
    if len(sys.argv) > 1:
        print("Usage:")
        print("  python3 src/vogon_poetry_v1.py <input_file> [output_directory] [--config-file config.json]")
        return

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Default configuration file (empty for no custom settings, or use stdin if provided via --input-only flag not supported here)
    config_file = "config.json"

    try:
        generator = AbstractDataTypeGenerator(input_path=input_path, output_dir=output_dir)
        
        print("Generating poetry...")
        result = generator.generate()
        
        # Output the generated data as a single string or list depending on needs. 
        # Here we use a simple JSON-like representation for compatibility with Python 3's json module if desired,
        # but since this is pure code generation without external libraries beyond sys.path (which includes 'json' in some environments),
        # we'll output it as text to avoid dependency issues unless the user explicitly wants JSON.
        
        print(f"Output generated for {input_path} -> {output_dir}")
        if result:
            # Output a formatted string representation of the data structure
            json_str = json.dumps(result, indent=2)
            
            with open(output_dir / "poetry_output.json", 'w') as f:
                f.write(json_str + "\n")

    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
    except Exception as e:
        print(f"Unexpected error generating poetry:")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
