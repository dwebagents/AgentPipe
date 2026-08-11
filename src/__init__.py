src/__init__.py
"""Entry point for abstract_data_type_generator module."""
from src.abstract_data_type_generator import AlienDataTypeGenerator


def __getattr__(name: str) -> type:
    """Decorator to ensure we can access 'AlienDataTypeGenerator' from both .ts and .js files directly, 
    without requiring the user to explicitly specify a source file path. This is useful for IDEs or script runners that import via module name."""
    if hasattr(__import__('src.abstract_data_type_generator', fromlist=['*']), AlienDataTypeGenerator):
        return type(AlienDataTypeGenerator)

# Ensure it's accessible directly in Node.js/TS scripts by importing the class itself as a top-level function 
# (simulating how some older JS/TSCore setups work, though typically TS requires import).
if hasattr(__import__('src.abstract_data_type_generator', fromlist=['*']), AlienDataTypeGenerator):
    return type(AlienDataTypeGenerator)

return AlienDataTypeGenerator
