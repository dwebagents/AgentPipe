"""
encrypt_decrypt_module.py
=========================
A simple rotation cipher (Caesar cipher variant) module for encrypting
and decrypting text messages and files.

How it works:
  - Each alphabetic character is shifted forward (encrypt) or backward
    (decrypt) by a fixed numeric key in the 26-letter alphabet.
  - Non-alphabetic characters (digits, spaces, punctuation) are passed
    through unchanged.
  - Upper- and lower-case letters are handled independently so that
    case is preserved in the output.

Usage example:
    key = 3
    cipher = RotateCipher(key)
    encrypted = cipher.encrypt("Hello, World!")   # => "Khoor, Zruog!"
    original  = cipher.decrypt(encrypted)         # => "Hello, World!"
"""

import os
import random


# ---------------------------------------------------------------------------
# Key generation
# ---------------------------------------------------------------------------

def generate_key(length):
    """Generate a random alphabetic key string for use with RotateCipher.

    The key is composed of randomly selected upper- and lower-case ASCII
    letters.  Although RotateCipher only uses the *integer* shift value
    stored in ``self.key``, this helper can produce a human-readable key
    token that a caller could later convert to an integer (e.g. via
    ``sum(ord(c) for c in key) % 26``).

    Args:
        length (int): Number of characters in the generated key string.

    Returns:
        str: A random alphabetic string of the requested length.

    Example:
        >>> k = generate_key(8)
        >>> len(k)
        8
    """
    # Build the key by drawing one random letter at a time
    return ''.join(
        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        for _ in range(length)
    )


# ---------------------------------------------------------------------------
# Rotation cipher class
# ---------------------------------------------------------------------------

class RotateCipher:
    """A Caesar-style rotation cipher that shifts letters by a fixed key.

    Attributes:
        key (int): The number of positions each letter is rotated.
                   Positive values shift forward (A->D for key=3);
                   negative values shift backward.

    Example:
        >>> cipher = RotateCipher(13)   # ROT-13
        >>> cipher.encrypt("Hello")
        'Uryyb'
        >>> cipher.decrypt("Uryyb")
        'Hello'
    """

    def __init__(self, key):
        """Initialise the cipher with the given rotation key.

        Args:
            key (int): Rotation amount (number of alphabet positions to shift).
        """
        self.key = key

    def encrypt(self, message):
        """Encrypt a plaintext message by rotating each letter forward.

        Non-alphabetic characters are copied to the output unchanged.
        Case is preserved: upper-case letters remain upper-case, and
        lower-case letters remain lower-case after the shift.

        Args:
            message (str): The plaintext string to encrypt.

        Returns:
            str: The ciphertext string with each letter shifted by ``self.key``.

        Example:
            >>> RotateCipher(3).encrypt("abc XYZ!")
            'def ABC!'
        """
        encrypted = ""
        for char in message:
            if char.isalpha():
                # Choose the correct ASCII base depending on letter case
                ascii_offset = ord('A') if char.isupper() else ord('a')
                # Rotate forward within the 26-letter alphabet (mod 26 wraps around)
                new_char = chr((ord(char) - ascii_offset + self.key) % 26 + ascii_offset)
                encrypted += new_char
            else:
                # Non-alphabetic characters are kept as-is
                encrypted += char
        return encrypted

    def decrypt(self, message):
        """Decrypt a ciphertext message by rotating each letter backward.

        This is the exact inverse of :meth:`encrypt`.  Non-alphabetic
        characters are passed through unchanged and letter case is preserved.

        Args:
            message (str): The ciphertext string to decrypt.

        Returns:
            str: The recovered plaintext string.

        Example:
            >>> RotateCipher(3).decrypt("def ABC!")
            'abc XYZ!'
        """
        decrypted = ""
        for char in message:
            if char.isalpha():
                # Choose the correct ASCII base depending on letter case
                ascii_offset = ord('A') if char.isupper() else ord('a')
                # Rotate backward within the 26-letter alphabet (mod 26 wraps around)
                new_char = chr((ord(char) - ascii_offset - self.key) % 26 + ascii_offset)
                decrypted += new_char
            else:
                # Non-alphabetic characters are kept as-is
                decrypted += char
        return decrypted


# ---------------------------------------------------------------------------
# File-level helpers
# ---------------------------------------------------------------------------

def encrypt_file(input_filename, output_filename):
    """Read a plaintext file, encrypt its contents, and write to a new file.

    A fresh random key is generated for every call, so the same input file
    will produce different ciphertext each time.  The key is printed to
    stdout so the caller can record it for later decryption.

    Args:
        input_filename  (str): Path to the plaintext source file.
        output_filename (str): Path where the encrypted output will be written.

    Side effects:
        Prints the generated key to stdout.
        Creates (or overwrites) ``output_filename``.

    Example:
        >>> encrypt_file("secret.txt", "secret.enc")
        Key: 7
    """
    # Read the entire source file
    with open(input_filename, 'r') as file:
        message = file.read()

    # Generate a new random integer key in the range [1, 25]
    key = random.randint(1, 25)
    print(f"Key: {key}")

    # Encrypt and write the ciphertext to the output file
    cipher = RotateCipher(key)
    encrypted_message = cipher.encrypt(message)
    with open(output_filename, 'w') as file:
        file.write(encrypted_message)


def decrypt_file(input_filename, output_filename, key):
    """Read an encrypted file, decrypt its contents, and write to a new file.

    Args:
        input_filename  (str): Path to the encrypted source file.
        output_filename (str): Path where the decrypted output will be written.
        key             (int): The rotation key that was used during encryption.

    Side effects:
        Creates (or overwrites) ``output_filename``.

    Example:
        >>> decrypt_file("secret.enc", "recovered.txt", 7)
    """
    # Read the entire encrypted file
    with open(input_filename, 'r') as file:
        message = file.read()

    # Decrypt using the provided key and write the result
    cipher = RotateCipher(key)
    decrypted_message = cipher.decrypt(message)
    with open(output_filename, 'w') as file:
        file.write(decrypted_message)
