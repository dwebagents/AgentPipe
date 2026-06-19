import os

def generate_key(length):
    # Generate a random key for rotation cipher
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(length))

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

def encrypt_file(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        message = file.read()
    
    key = generate_key(len(message))
    cipher = RotateCipher(key)
    encrypted_message = cipher.encrypt(message)
    
    with open(output_filename, 'w') as file:
        file.write(encrypted_message)

def decrypt_file(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        message = file.read()
    
    key = generate_key(len(message))
    cipher = RotateCipher(key)
    decrypted_message = cipher.decrypt(message)
    
    with open(output_filename, 'w') as file:
        file.write(decrypted_message)

def main():
    encrypt_file('original.txt', 'encrypted.txt')
    decrypt_file('encrypted.txt', 'decrypted.txt')

if __name__ == "__main__":
    main()

# Klingon poetry
# Vek'tal na kai'men, na'kathro, u'tar'gat.
