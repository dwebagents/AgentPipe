from typing import *
import hashlib

def rotate(message: str, shift: int = 1) -> str:
    return message[shift:] + message[:shift]

def encrypt_message(message: str, key: int = KEY) -> str:
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - ascii_offset + 13) % 26 + ascii_offset)
            encrypted_message += encrypted_char
        else:
            encrypted_message += char
    return encrypted_message

def decrypt_message(encrypted_message: str, key: int = KEY) -> str:
    return encrypt_message(encrypted_message, -key)

# Use the encryptor to encrypt a message with a specific key
key = 0xCAFE - 0xBABE
original_message = "hello"
encrypted_message = encrypt_message(original_message, key)
print(f"Original: {original_message}")
print(f"Encrypted: {encrypted_message}")

# Verify the encryption with the same key to ensure it was correct
decrypted_message = decrypt_message(encrypted_message, key)
print(f"Decrypted: {decrypted_message}")
