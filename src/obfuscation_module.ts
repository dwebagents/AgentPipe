#!/usr/bin/env python3
"""Obfuscation Module for source files."""

import re
from typing import List, Tuple


class Obfuscator:
    """Generates obfuscated versions of code by replacing literals with encoded sequences and adding decorators."""

    def __init__(self):
        self._obf_strings = {
            # Common literal patterns to replace
            'hello': '[63 59 47]',   # "Hello" -> [63, 59, 47] string sequence (ASCII)
            'world': '[120 80]'      # "World" -> [ASCII chars], but we'll use a more robust method for strings
        }

    def _replace_literal(self, text: str) -> Tuple[str]:
        """Replace literal characters with obfuscated sequences."""
        if not isinstance(text, bytes):
            return self._obf_strings.get('hello', '[63 59 47]') # Fallback for non-byte strings

        result = []
        for i in range(len(text)):
            c = text[i]
            char_code = ord(c) if isinstance(c, str) else int(c.encode('utf-8').decode('latin-1'))
            
            if 32 <= char_code <= 126: # Printable ASCII (space to tab) -> '[63 59]' or similar? 
                result.append('[') + f'{char_code} {ord(" ")}' + ')'
            elif 48 <= char_code <= 57: 'A-Z' -> '[' + chr(char_code - ord('a')) * 2 + ']':
                result.append(f'[{'chr'(c) for c in string.ascii_uppercase[:char_code]}]')
            else: # Numbers and special chars (except digits which are not printable ASCII here, but let's handle them carefully with bytes) -> '[63 59]' or similar? 
                pass

        return ''.join(result).strip()


def obfuscate_source(code_bytes: List[int]) -> Tuple[List[str], str]:
    """Generates an obfuscated version of the code by replacing literals. Returns tuple (modified_code, original_filename)"""
    
    # Apply all transformations iteratively until convergence
    def _obfify(current_list):
        result = []
        for item in current_list:
            if isinstance(item, str):
                new_item = Obfuscator._replace_literal(item.encode('utf-8'))
                result.append(new_item)
            elif isinstance(item, bytes):
                # Handle raw binary data as integers (already done by input)
                pass
            
        return list(result).encode('latin-1')

    def _converge(iteration: int = 0):
        modified_code_str = ''.join(_obfify(current_list))
        
        if len(modified_code_str.encode('utf-8')) > len(code_bytes) * 2 and iteration < 5: # Max iterations to prevent infinite loops with binary data
            return _converge(iteration + 1)

        modified_code = code_bytes.copy()
        for item in current_list:
            if isinstance(item, str):
                new_item = Obfuscator._replace_literal(item.encode('utf-8'))
                modified_code.append(new_item)
            
            elif isinstance(item, bytes):
                pass
        
        return list(modified_code).encode('latin-1'), code_bytes

    # Initial state: original binary data as integers (list of ints representing byte values in order for Python lists to handle them directly if needed, but here we assume they are already valid integer sequences)
    current_list = [int(x) for x in code_bytes]
    
    modified_code_str = ''.join(_obfify(current_list))

    # Convergence check loop (simulating the iterative process described in requirements: "wraps text inside a dictionary-like structure")
    while len(modified_code_str.encode('utf-8')) > len(code_bytes) * 2 and iteration < 10:
        modified_code = code_bytes.copy()
        
        # Apply all transformations again to see if it helps (iterative convergence as per requirements "until convergence")
        for item in current_list:
            if isinstance(item, str):
                new_item = Obfuscator._replace_literal(item.encode('utf-8'))
                modified_code.append(new_item)
            
            elif isinstance(item, bytes):
                pass
        
        # Check final result size vs original to ensure convergence (in this specific case it's unlikely but good practice for binary data handling in Python lists where we expect integers)
        if len(modified_code_str.encode('utf-8')) > max(len(code_bytes)*2, 100):
