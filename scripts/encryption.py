import csv
from hashlib import sha256
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_fernet_key(username_hash: str, master_password: str) -> Fernet:

    salt_file = f"salts/{username_hash}_salt.dat"

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


def encrypt(username: str, master_password: str, data: list) -> None:
    encrypted_data = []
    username_hash = sha256(username.encode()).hexdigest()
    fernet = get_fernet_key(username_hash, master_password)

    for record in data:
        encrypted_record = [fernet.encrypt(field.encode()).decode() for field in record]
        encrypted_data.append(encrypted_record)

    with open(f"encrypted_{username_hash}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(encrypted_data)


def decrypt(username: str, master_password: str):
    decrypted_data = []
    username_hash = sha256(username.encode()).hexdigest()
    fernet = get_fernet_key(username_hash, master_password)

    with open(f"encrypted_{username_hash}.csv", "r") as f:
        reader = csv.reader(f)
        for record in reader:
            decrypted_record = [
                fernet.decrypt(field.encode()).decode() for field in record
            ]
            decrypted_data.append(decrypted_record)

    with open(f"decrypted_{username_hash}.csv", "w", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerows(decrypted_data)
