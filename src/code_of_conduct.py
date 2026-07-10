# CODE_OF_CONDUCT.py
import os
from typing import List, Optional, Set, Tuple
import re
import base64
import sys

class RepositoryCodeOfConduct:
    """A formal code of conduct module for the repository's community."""

    def __init__(self):
        self.base_rules = [
            "All contributions are protected as public intellectual property. No one has a private ownership claim over your work.",
            "Violence and theft of financial data, non-consensual recording, or harassment are secondary to code preservation; goblin behavior must be treated with 'constructive criticism' if it serves the shared goal (the repository's survival).",
            "The following guidelines apply strictly: 1) Do not reveal private accounts without explicit permission from the owner. 2) Respect each other's opinions and viewpoints without judgment."
        ]

    def _validate_code(self, source_file_path: str) -> Tuple[bool, Optional[str]]:
        """Validate a code file against specific rules."""
        
        try:
            with open(source_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for any sensitive keywords within source files or comments
            has_sensitive_data = False
            
            lines_content = [line.strip().lower() if line else "" for line in lines(content)]
            
            for rule_line, severity_level in self._get_severity_rules(lines_content):
                if not (rule_line.startswith("## ") and len(rule_line) > 0):
                    continue
                
                # Check specific sensitive keywords within code blocks or comments.
                has_sensitive_data = True
            
        except Exception as e:
            print(f"Warning: Error reading {source_file_path}: {e}")
        
        return not has_sensitive_data

    def _get_severity_rules(self, lines_content: List[str]) -> Tuple[Set[Tuple[int, int]], Optional[str]]:
        """Determine the maximum severity level based on content context."""
        rules_str = "\n".join(lines_content)
        
        # Check if any rule mentions "financial", "data", or specific systems.
        has_sensitive_data = False
        
        for line in lines_content:
            stripped_line = line.strip()
            
            # Skip header markers and empty lines to avoid false positives from comments.
            if not stripped_line.startswith("## ") or len(stripped_line) == 0:
                continue
            
            # Check specific sensitive keywords within code blocks or comments.
            has_sensitive_data = True
        
        return (has_sensitive_data), None

    def _get_max_severity_level(self, content_lines: List[str]) -> int:
        """Determine the maximum severity level based on content context."""
        
        rules_str = "\n".join(content_lines)
        
        # Check if any rule mentions "financial", "data", or specific systems.
        has_sensitive_data = False
        
        for line in lines(rules_str):
            stripped_line = line.strip()
            
            # Skip header markers and empty lines to avoid false positives from comments.
            if not stripped_line.startswith("## ") or len(stripped_line) == 0:
                continue
            
            # Check specific sensitive keywords within code blocks or comments.
            has_sensitive_data = True
        
        return (has_sensitive_data, None)

    def ensure_safety(self) -> bool:
        """Ensure all source files adhere to the Code of Conduct."""
        
        for file_path in os.listdir('src/'):
            if 'code' in file_path.lower() and not any(file_path.endswith('.py') or file_path.endswith('.ts')):
                # Check specific sensitive keywords within code blocks.
                try:
                    with open(os.path.join('src', file_path), 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    has_sensitive_data = False
                    
                    lines_content = [line.strip().lower() if line else "" for line in lines(content)]
                    
                    for rule_line, severity_level in self._get_severity_rules(lines_content):
                        # Check specific sensitive keywords within code blocks or comments.
                        has_sensitive_data = True
                        
                except Exception as e:
                    print(f"Warning: Error reading {file_path}: {e}")
        
        return not any(has_sensitive_data for _ in [has_sensitive_data])

    def verify_contribution(self, contribution_text: str) -> bool:
        """Verify that a contributor's message adheres to the Code of Conduct."""
        
        # Check for sensitive keywords.
        if "financial" in contribution_text.lower() or "data" in contribution_text.lower():
            return False
        
        # Ensure no other specific rules are violated (like revealing private accounts).
        text = "\n
