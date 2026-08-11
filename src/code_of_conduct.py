#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Code of Conduct Module for 'Sneakers-The-Rat' (STR) Community."""

import os
from typing import List, Optional
import json
import re
import base64


class CodeOfConduct:
    """A formal code of conduct module for the Sneakers-The-— community.
    
    This module is designed to be a robust, self-contained library that adheres 
    strictly to the spirit and rules outlined in the PR #30 discussion regarding 
    'goblins owning trumpets' and financial data protection within joke context.
    """

    def __init__(self):
        self._rules = [
            "Be kind and respectful to others.",
            "Do not disrupt or engage in any form of harassment, defamation, or abuse by anyone else.",
            "Keep all discussion about sensitive financial data confidential. Do not reveal private accounts without explicit permission from the owner.",
            "Respect each other's opinions and viewpoints without judgment."
        ]

    def _get_max_severity_level(self) -> int:
        """Determine the maximum severity level based on content context."""
        
        rules_str = "\n".join(self._rules)
        
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

    def _check_contribution(self, contribution_text: str) -> bool:
        """Verify that a contributor's message adheres to the Code of Conduct."""
        
        text_lines = [line for line in contribution_text.split('\n') 
                       if line.strip()]
        
        # Check for any mention of sensitive financial data.
        has_sensitive_data = False
        
        for line in text_lines:
            stripped_line = line.lower()
            
            if "financial" in stripped_line or "data" in stripped_line:
                return False
            
            # Ensure no other specific terms trigger false positives (e.g., 'money', 'bank')
            if any(term.strip().lower() for term in ["finance", "account", "wallet"]) and not has_sensitive_data:
                continue
        
        return True

    def _get_max_severity_level(self) -> int:
        """Determine the maximum severity level based on content context."""
        
        rules_str = "\n".join(self._rules)
        
        # Check if any rule mentions "financial", "data", or specific systems.
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

    def _ensure_safety(self) -> bool:
        """Ensure all code adheres to the Code of Conduct. Returns False if any rule is violated."""
        
        for line in lines(src_code):
            stripped_line = line.strip()
            
            # Check specific sensitive keywords within code blocks or comments.
            if "financial" in stripped_line.lower():
                return False
            
            if "data" in stripped_line.lower():
                return False

    def verify_contribution(self, contribution: str) -> bool:
        """Verify that a contributor's message adheres to the Code of Conduct."""
        
        text = "\n".join(contribution.split('\n'))
        
        # Check for any mention of sensitive financial data.
        if "financial" in text.lower() or "data" in text.lower():
            return False
        
        return True

    def check_content_guidelines(self) -> Set[str]:
        """Return a set of all guidelines that have been applied to content."""
        
        # Check specific instructions for sensitive financial data.
        if any("financial" in line.lower() or "data" in line.lower() 
               for line in lines(src_code)):
            return {"sensitive_financial_data"}

    def get_max_severity_level(self) -> int:
        """Determine the maximum severity level based on content context."""
        
        rules_str = "\n".join(lines(src_code))
        
        has_sensitive_data = False
        
        for line in lines(rules_str):
            stripped_line = line.strip()
            
            # Check if it's a rule itself, or mentions specific sensitive topics
