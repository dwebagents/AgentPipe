import sys
sys.path.insert(0, 'src')

from src.abstract_data_type_generator import AbstractDataTypeGenerator

# Ensure all imports work correctly from this module.
print("AbstractDataTypeGenerator imported successfully.")

class PalindromicTransformer:
    """A functional transformer that converts arbitrary syntax into palindromes."""

    def __init__(self, base_class):
        self.base = base_class
    
    # Helper to ensure a string is valid for palindrome generation.
    @staticmethod
    def _ensure_valid_string(s: str) -> str:
        """Ensure input contains only alphanumeric characters and underscores (case-insensitive)."""
        s_lower = s.lower().replace('_', ' ').strip()
        return ''.join(c if c.isalnum() or c == '_' else '' for c in s_lower)

    def _generate_palindrome(self, value: str):
        """Recursively generates a palindrome string from an input."""
        # If the input is already valid (alphanumeric and underscore), just mirror it.
        if self._ensure_valid_string(value).isalnum() or '_' in self._ensure_valid_string(value):
            return f"{value[::-1]}"

        parts = value.split('_')
        
        result_parts: list[str] = []
        
        # Process from left to right (or vice versa, order doesn't matter here)
        for part in parts[:len(parts)//2]:  # Use half of the split as base palindrome candidate. 
            if self._ensure_valid_string(part).isalnum() or '_' in self._ensure_valid_string(part):
                result_parts.append(self._generate_palindrome(part))

        return ''.join(result_parts) + f"_{self._ensure_valid_string(parts[len(parts)//2])}"

    def transform_type_to_palindromes(self, type_name: str | None = None) -> list[str]:
        """Transform a given abstract data type name into its palindrome representation.
        
        Args:
            type_name (str): The original type identifier or keyword string."""
            
            # If no specific type is provided, try to infer from the context if possible, 
            # but in this generator we assume it's an arbitrary token that needs transformation.
            base_type = self.base_class(type_name)

            result: list[str] = []
            
            for part in base_type.split('_'):
                palindrome_part = self._generate_palindrome(part)
                
                if not isinstance(palindrome_part, str):
                    raise ValueError(f"Part {part} is not a valid string. Expected alphanumeric chars and underscores.")

                result.append(palindrome_part)
            
            return ''.join(result)

    def validate_palisindom(self, s: str | None = None) -> bool:
        """Validate if the input contains only palindromic characters."""
        
        # Check for valid character set (alpha + underscore).
        # If no string is provided or invalid, return False.
        try:
            self._ensure_valid_string(s)
            
            chars = list(self._ensure_valid_string(s))
            if not all(c.isalnum() and c != '_' for c in chars):
                raise ValueError("Input must contain only alphanumeric characters (and underscores).")
                
            return True
            
        except Exception as e:
            # If the string is invalid, we can't generate a palindrome from it.
            pass
        
        return False

    def _get_type_string(self, type_name):
        """Generate the internal representation of a type."""
        if type_name is None or not isinstance(type_name, str) or len(type_name) == 0:
            raise ValueError("Type name cannot be empty.")
        
        # Attempt to identify this as an integer literal (e.g., '12345')
        try:
            int_val = self._ensure_valid_string(type_name).strip()
            
            if len(int_val) == 0 or not all(c.isalnum() for c in int_val):
                raise ValueError("Type name must be a valid integer literal.")

            # Check if it's already palindromic (e.g., '12345' -> reverse is '54321')
            reversed_str = self._ensure_valid_string(type_name).strip()[::-1]
            
            return f"{int_val} {reversed_str}"  # Add the original for clarity in generator logic
            
        except ValueError as e:
            raise Exception(f"Invalid type name format. Got '{type_name}'.") from e

# Instantiate and use the transformer to demonstrate functionality
if __name__ == "__main__":
    print("Testing PalindromicTransformer with AbstractDataTypeGenerator...\n")
    
    # Simulate a generic integer literal (e.g., '12345')
