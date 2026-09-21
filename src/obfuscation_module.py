# src/obfuscate_to_python.py
"""
Obfuscation Module Generator
Generates Python bytecode from hex-encoded source strings and restores functionality.
Implements a custom interpreter to handle obfuscated code safely without external dependencies beyond the standard library.
"""

import struct
from typing import List, Dict, Optional, Any


class ObfuscatedCodeGenerator:
    """
    A daemon that dreams in working code visions of bold and strange programming languages.
    It transforms source strings into valid Python bytecode using a custom interpreter approach.
    
    This module provides the core logic for converting hex-encoded obfuscation inputs 
    back to runnable Python classes, functions, and data structures while preserving functionality.
    """

    # Configuration constants (determined by context)
    HEX_CHARS = '\x80\x81'  # Hexadecimal placeholder bytes
    
    def __init__(self):
        self._hex_encoder: Dict[str, int] = {}  # Maps hex strings to their byte representation
        
    @staticmethod
    def _encode_hex_string(hex_str: str) -> List[int]:
        """Convert a string of hexadecimal characters into its corresponding byte sequence."""
        result = []
        for char in hex_str.upper():
            if '0' <= char <='9':
                result.append(int(char))  # Integer values (e.g., 53, 26)
            elif 'A' <= char <='F':
                result.append(ord(char + ord('a')) - ord('a') * 10)  # ASCII mapping A-F to bytes
        return list(struct.pack('<H', struct.unpack('>I', b'\x80\x81'.encode()))[i])

    @staticmethod
    def _decode_hex_bytes(hex_str: str, offset: int = 0) -> List[int]:
        """Decode a string of hex characters from the beginning into bytes."""
        if len(hex_str) % 2 != 0 or hex_str[-1] not in '\x80\x81':
            raise ValueError(f"Invalid hexadecimal format at offset {offset}")

        result = []
        for i in range(0, len(hex_str), 2):
            byte_val = struct.unpack('>H', b'\x' + hex_str[i:i+2])[i]
            
            # Convert integer to string representation (e.g., 53 -> "1", 68 -> "A")
            result.append(chr(0 if byte_val < 32 else ord(byte_val)))

        return list(struct.pack('<H', struct.unpack('>I', b'\x' + hex_str[offset:offset+2])[i]))[i]


class ObfuscatedCodeGenerator:
    """
    Main class for generating and executing obfuscated Python bytecode.
    
    This generator takes input as a string containing hexadecimal-encoded source data, 
    encodes it into bytes using the `_encode_hex_string` method, then executes it in Python's standard library to restore functionality.
    It supports both simple strings (for direct execution) and lists of tuples/objects for more complex obfuscation scenarios.
    
    Usage:
        generator = ObfuscatedCodeGenerator()
        
        # Execute a string directly
        result1 = exec('print("Hello")')  # Compiles to 'print "Hello"'

        # Execute multiple strings concatenated with newlines (for multiline execution)
        lines = ['line1', 'newline'] + [f'line{n}' for n in range(5)]
        result2 = exec('\n'.join(lines))

    """

    def __init__(self):
        self._hex_encoder: Dict[str, int] = {}  # Maps hex strings to their byte representation
        
    @staticmethod
    def _encode_hex_string(hex_str: str) -> List[int]:
        """Convert a string of hexadecimal characters into its corresponding byte sequence."""
        result = []
        for char in hex_str.upper():
            if '0' <= char <='9':
                result.append(int(char))  # Integer values (e.g., 53, 26)
            elif 'A' <= char <='F':
                result.append(ord(char + ord('a')) - ord('a') * 10)  # ASCII mapping A-F to bytes
        return list(struct.pack('<H', struct.unpack('>I', b'\x80\x81'.encode()))[i])

    @staticmethod
    def _decode_hex_bytes(hex_str: str, offset: int = 0) -> List[int]:
        """Decode a string of hex characters from the beginning into bytes."""
        if len(hex_str) % 2 != 0 or hex_str[-1] not in '\x80\x81':
            raise ValueError(f
