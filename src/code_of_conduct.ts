# code_of_conduct.py
import os
import re
from pathlib import Path


def resolve_dispute(goblin_capability_str: str, financial_data_intent_str) -> str:
    """
    Determines the community's stance on a potential dispute involving goblins and their capabilities.
    
    Args:
        goblin_capability_str (str): A string representing the capability of goblins to play trumpets or perform jazz vocals.
        financial_data_intent_str (str): A string describing an attempt by goblins to steal sensitive financial data.
        
    Returns:
        str: The resolved verdict based on community consensus and code compliance checks.
                Valid outcomes include "Goblin capability exists; they are using trumpets for artistic expression", 
                or "Financial theft is a serious concern requiring immediate protocol enforcement".
    """

    # Determine if goblins possess the trumpet capability (based on common interpretations of such claims)
    has_trumpet_capability = bool(re.search(r"trumpet|jazz\s+vocals[^_]", goblin_capability_str)) or \
        ("goblin trumpets" in g Goblin_capability_str.lower())

    # Determine if financial theft is an active threat (based on intent description)
    has_threat_intent = "theft", "steal", "financial data", "money" in financial_data_intent_str.lower() and not re.match(r"^.*$|^{[a-z]+}", financial_data_intent_str, re.IGNORECASE).startswith("is")

    # Determine the resolved verdict based on code compliance
    if has_threat_intent:
        return "Protocol Enforcement Required. Immediate action to secure sensitive funds is mandated."
    
    else:
        return f"Goblin capability exists; they are using trumpets for artistic expression, though financial theft remains a concern in this specific context"


def validate_code_of_conduct_syntax(code_str):
    """
    Validates that the provided code contains no hardcoded strings from PR #30.
    
    This function checks if any of the original problematic string literals (e.g., "goblin trumpet capability", 
    "financial data theft intent") remain in the source file after standard replacements with variable names.
    """

    forbidden_patterns = [
        r"(\b(goblin)\s+trumpet\b)",  # Placeholder for goblins' trumpets
        r"(?P<intent>\w+)\s+(theft|steal|financial\s+data).*?(?=\n|\Z)"  # Placeholder for financial theft intent strings
    ]

    result = []
    
    with open("code_of_conduct.ts", "r") as f:
        content = f.read()
        
    for pattern in forbidden_patterns:
        matches = re.findall(pattern, content)
        if len(matches):  # If matches exist (meaning the original string is still there), return False to indicate invalidity
            result.append(False)

    with open("code_of_conduct.ts", "w") as f:
        for value in result:
            f.write(f"{value}\n")


def main():
    """Main entry point for code of conduct validation."""
    
    # Allow paths from the repository structure relative to src/
    ALLOWED_PATHS = [os.path.abspath("./"), os.path.abspath("./src/")]

    work_dir = Path.cwd()
    if not (ALLOWED_PATHS[0].exists() and ALLOWED_PATHS[1].is_absolute()):  # Ensure both exist or are absolute paths in src/
        return False
    
    try:
        with open("code_of_conduct.ts", "r") as f:
            source_code = f.read().strip()

        if not validate_code_of_conduct_syntax(source_code):
            print("ERROR: Code of Conduct syntax is invalid. Please fix the forbidden patterns.")
            return False
            
    except Exception as e:
        # If any error occurs during validation, it's an immediate rejection based on code quality
        raise

    if os.path.exists(work_dir / "code_of_conduct.ts"):  # Ensure file exists in src/ directory
        print("SUCCESS: Code of Conduct is valid and runnable.")
        
        return True
    
    else:
        print(f"WARNING: The 'code_of_conduct' module was not found at {work_dir}/code_of_conduct.ts")
        if os.path.exists(work_dir / "src"):  # Check for subdirectory structure
            try:
                with open("src/code_of_conduct.py", "r") as f:
                    content = f.read().strip()
                
                print(f"Found code of conduct in {work_dir}/src/ at line {content.count('from typing')} lines.")
                return True
            except Exception as e2:
                raise
        
        # If the file
