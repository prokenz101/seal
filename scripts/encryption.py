from base64 import urlsafe_b64encode
from hashlib import sha256

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_fernet_key(master_password, salt_file):
    """Generate a Fernet key from the master password and salt file."""

    with open(salt_file, "rb") as f:
        salt = f.read()

    #* Deriving a key from the master password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = urlsafe_b64encode(kdf.derive(master_password.encode()))
    fernet = Fernet(key)
    return fernet


def encrypt(username, master_password, data):
    """Encrypt a string using the user's master password and a unique salt."""

    username_hash = sha256(username.encode()).hexdigest()
    fernet = get_fernet_key(master_password, f"salts/{username_hash}_salt.dat")
    encrypted_data = fernet.encrypt(data.encode()).decode()
    return encrypted_data


def encrypt_data(username, master_password, data):
    """Encrypt a list of strings using the user's master password and a unique salt."""

    encrypted_data = []

    for record in data:
        encrypted_record = [
            encrypt(username, master_password, field) for field in record
        ]
        encrypted_data.append(encrypted_record)

    return encrypted_data


def decrypt(username, master_password, data):
    """Decrypt a string using the user's master password and a unique salt."""

    username_hash = sha256(username.encode()).hexdigest()
    fernet = get_fernet_key(master_password, f"salts/{username_hash}_salt.dat")
    decrypted_data = fernet.decrypt(data.encode()).decode()
    return decrypted_data


def decrypt_data(username, master_password, data):
    """Decrypt a list of strings using the user's master password and a unique salt."""

    decrypted_data = []
    username_hash = sha256(username.encode()).hexdigest()
    fernet = get_fernet_key(master_password, f"salts/{username_hash}_salt.dat")

    for record in data:
        decrypted_record = [fernet.decrypt(field.encode()).decode() for field in record]
        decrypted_data.append(decrypted_record)

    return decrypted_data
