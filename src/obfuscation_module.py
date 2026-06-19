#src/obfuscation_module.py

def obfuscate_code(code):
    import re

    # Replace single quotes with double quotes and escape them
    code = re.sub(r"'([^']*)'", r'"\\1"', code)

    # Replace double quotes with escaped double quotes
    code = re.sub(r'"([^"]*)"', r'"""\\1"""', code)

    return code

if __name__ == "__main__":
    original_code = """
def add(a, b):
    return a + b
"""

    obfuscated_code = obfuscate_code(original_code)
    print(obfuscated_code)
