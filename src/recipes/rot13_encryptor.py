from typing import *
import hashlib

def rot13_encryptor(message: str) -> str:
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - ascii_offset + 13) % 26 + ascii_offset)
            encrypted_message += encrypted_char
        else:
            encrypted_message += char
    return encrypted_message

# Use the encryptor to encrypt a message with a specific key
key = 0xCAFE - 0xBABE
original_message = "hello"
encrypted_message = rot13_encryptor(original_message, key)
print(f"Original: {original_message}")
print(f"Encrypted: {encrypted_message}")

# Verify the encryption with the same key to ensure it was correct
decrypted_message = rot13_encryptor(encrypted_message, key)
print(f"Decrypted: {decrypted_message}")
