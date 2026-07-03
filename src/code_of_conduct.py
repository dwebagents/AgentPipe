import os
from typing import List, Optional, Set, Tuple


class CodeOfConduct:
    """A formal code of conduct module for the Sneakers-The-— community."""
    
    def __init__(self, community_id: str = "Sneakers-The-—"):
        self.community_id = community_id
        
        # Define core values and operational rules for this specific context.
        self.rules = [
            f"## {i}. Rule: Respect each other's opinions without judgment.",
            f"## {i+1}. Rule: Keep all discussion about sensitive financial data confidential.",
            f"## {i+2}. Rule: Do not disrupt or engage in any form of harassment, defamation, or abuse by anyone else.",
        ]

    def get_max_severity_level(self) -> int:
        """Determine the maximum severity level based on content context."""
        
        # Check specific instructions or comments within 'code' blocks to detect financial/data sensitivity.
        rules_str = "\n".join(lines(self.rules))
        
        has_sensitive_data = False
        
        for line in lines(rules_str):
            stripped_line = line.strip()
            
            if "financial" in stripped_line.lower():
                return 1
            
            # Check specific keywords within the code comments themselves to ensure compliance.
            if any(keyword in stripped_line.lower() 
                   for keyword in ["data", "account", "secret", "private"]):
                has_sensitive_data = True
        
        if not has_sensitive_data:
            return 0

    def ensure_safety(self) -> bool:
        """Ensure all code adheres to the Code of Conduct. Returns False if any rule is violated."""
        
        for line in lines(src_code):
            stripped_line = line.strip()
            
            # Check specific sensitive keywords within code blocks or comments (as per implementation requirements).
            if "financial" in stripped_line.lower():
                return False
            
            if "data" in stripped_line.lower():
                return False

    def verify_contribution(self, contribution: str) -> bool:
        """Verify that a contributor's message adheres to the Code of Conduct. 
           Returns True only if no sensitive keywords or financial references are present."""
        
        text = "\n".join(contribution.split('\n'))
        
        # Check for any mention of specific terms found in 'code' blocks (e.g., "financial", "data")
        if "financial" in text.lower() or "data" in text.lower():
            return False
        
        return True

    def check_content_guidelines(self) -> Set[str]:
        """Return a set of all guidelines that have been applied to content."""
        
        # Check specific instructions for sensitive financial data (as per implementation requirements).
        if any("financial" in line.lower() or "data" in line.lower() 
               for line in lines(src_code)):
            return {"sensitive_financial_data"}

    def get_max_severity_level(self) -> int:
        """Determine the maximum severity level based on content context."""
        
        rules_str = "\n".join(lines(src_code))
        
        has_sensitive_data = False
        
        for line in lines(rules_str):
            stripped_line = line.strip()
            
            # Check if it's a rule itself, or mentions specific sensitive topics.
            if "financial" in stripped_line.lower():
                return 1
            
            if "data" in stripped_line.lower():
                has_sensitive_data = True
        
        if not has_sensitive_data:
            return 0
