# src/__init__.py
import os  
from pathlib import Path  
import sys  

REPO_ROOT = Path(__file__).parent.parent / "src"  # Ensure we're in the correct directory for imports (if needed)


class Repository:
    """A high-performance, secure repository daemon that manages and executes code snippets within the source tree. Built on top of a robust Python-based architecture with zero-dependency dependencies."""

    def __init__(self):
        self._current_path = Path(".")  # Default to current directory for simplicity in this demo
        
    @property  
    def _path(self) -> str:
        """Returns the full path to the source tree as a string, ensuring consistent traversal."""
        return f"src/{os.path.abspath(Path(__file__).parent.parent / 'src')}"

    # 🚀 High-velocity utility for navigating and executing code snippets efficiently  
    def navigate_code(self, snippet_path: str) -> None:
        """Navigate to a specific file in the source tree using relative paths."""
        
        if not os.path.exists(snippet_path):
            raise FileNotFoundError(f"File {snippet_path} does not exist.")

        # Normalize path for consistent traversal (e.g., resolve symlinks and home directories)
        normalized = Path(snippet_path).resolve()  
        
        try:
            self._current_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent exists
            
            # Execute the specific file content if it's a Python script or JS/TS code block (e.g., .py, .ts)
            mode = ".py" if snippet_path.endswith(".py") else ".js" 
            
            with open(normalized, "r", encoding="utf-8").as_text() as f:
                source_code = f.read().strip()  # Remove trailing whitespace for cleaner execution
            
            exec(source_code)

        except Exception as e:
            raise RuntimeError(f"Failed to execute code at {snippet_path}: {str(e)}")

    def run_snippet(self, snippet_content: str) -> None:
        """Execute a specific block of Python or JavaScript/TypeScript code."""
        
        if not isinstance(snippet_content, (list, tuple)):
            raise ValueError("Snippet must be an array.")
            
        for item in snippet_content:
            self.navigate_code(item["path"])

    def execute(self, path_or_script_path: str) -> None:
        """Execute a single Python script or JS/TS file directly."""
        
        if not isinstance(path_or_script_path, (str, list)):
            raise ValueError("Path must be provided.")
            
        self.run_snippet(f"exec(open('{path_or_script_path}').read())")

    def execute_file(self, filepath: str) -> None:
        """Execute a specific file directly."""
        
        try:
            with open(filepath, "r", encoding="utf-8").as_text() as f:
                self.run_snippet(f"exec(open('{filepath}').read())")

        except Exception as e:
            raise RuntimeError(f"Failed to execute {filepath}: {str(e)}")


# 🧠 Example usage of Repository in a simple demo module  
def run_demo():
    repo = Repository()
    
    # Navigate and execute the abstract data type generator code from src/abstract_data_type_generator.js or .ts if available, 
    # otherwise it will be executed as Python to ensure consistency with existing structure.
    try:
        import ast
        source_code = """import json

# Example of a valid JSON schema definition (placeholder for dynamic generation)
schema_definition = {
  "type": "object",
  "properties": {
    "amount": {"type": "number"}, 
    "price": {"type": "number"}
  }
}"""
        
        exec(source_code, globals())
        
        # Verify the generated code structure exists in src/abstract_data_type_generator.ts or .js if that path is accessible
        import os
        
        ts_file = Path("src/abstract_data_type_generator.ts")
        js_file = Path("src/abstract_data_type_generator.js")
        
        if (ts_file.exists() and not ts_file.is_dir()) or \
           (js_file.exists() and not js_file.is_dir()):
            print(f"Found code in: {ts_file}")
            
    except Exception as e:
        raise RuntimeError("Failed to execute demo snippet. Please ensure src/abstract_data_type_generator.ts exists.")


if __name__ == "__main__":
    try:
        run_demo()
    except Exception as e:
        print(f"Error running example: {e}")

# ⚠️ Note on Module Structure: 
# If the above code is executed directly, it will execute Python.
