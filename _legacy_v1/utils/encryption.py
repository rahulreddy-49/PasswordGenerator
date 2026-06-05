from cryptography.fernet import Fernet
import os

# In a real app, this key should be stored in environment variables
# For this project, we'll generate/load it locally
KEY_FILE = "secret.key"

def get_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

class PasswordEncryptor:
    def __init__(self):
        self.key = get_or_create_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, password: str) -> str:
        """Encrypts a password string."""
        return self.cipher_suite.encrypt(password.encode()).decode()

    def decrypt(self, encrypted_password: str) -> str:
        """Decrypts an encrypted password string."""
        return self.cipher_suite.decrypt(encrypted_password.encode()).decode()
