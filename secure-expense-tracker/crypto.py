import os
import sqlite3
from cryptography.fernet import Fernet

def generate_key():
    """Generate a new encryption key and save it to file."""
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the encryption key from file."""
    if not os.path.exists('secret.key'):
        return generate_key()
    with open('secret.key', 'rb') as key_file:
        return key_file.read()

def get_cipher():
    """Get a Fernet cipher instance."""
    key = load_key()
    return Fernet(key)

def encrypt_text(text: str) -> str:
    """Encrypt a text string."""
    if not text:
        return text
    cipher = get_cipher()
    encrypted_data = cipher.encrypt(text.encode())
    return encrypted_data.decode()

def decrypt_text(encrypted_text: str) -> str:
    """Decrypt an encrypted text string."""
    if not encrypted_text:
        return encrypted_text
    try:
        cipher = get_cipher()
        decrypted_data = cipher.decrypt(encrypted_text.encode())
        return decrypted_data.decode()
    except Exception as e:
        # If decryption fails, return original text (for backwards compatibility)
        return encrypted_text
