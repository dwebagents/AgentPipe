from typing import *
import random

class RotateCipher:
    def __init__(self, key):
        self.key = key
    
    def encrypt(self, message):
        encrypted = ""
        for char in message:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                new_char = chr((ord(char) - ascii_offset + self.key) % 26 + ascii_offset)
                encrypted += new_char
            else:
                encrypted += char
        return encrypted
    
    def decrypt(self, message):
        decrypted = ""
        for char in message:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                new_char = chr((ord(char) - ascii_offset - self.key) % 26 + ascii_offset)
                decrypted += new_char
            else:
                decrypted += char
        return decrypted

# Example usage
cipher = RotateCipher(KEY)
original_message = "HELLO WORLD!"
encrypted_message = cipher.encrypt(original_message)
print("Encrypted:", encrypted_message)

decrypted_message = cipher.decrypt(encrypted_message)
print("Decrypted:", decrypted_message)
