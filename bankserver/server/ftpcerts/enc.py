    # Start the main loop
    
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from bcrypt import hashpw, gensalt
from secrets import randbits

def encrypt_private_key(private_key: bytes, passphrase: str) -> tuple[bytes,bytes,bytes]:
    # Use PBKDF2 to derive a key from the passphrase
    salt = gensalt()
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode())
    
    # Encrypt the private key with AES
    iv = randbits(128)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_private_key = encryptor.update(private_key) + encryptor.finalize()
    
    return (encrypted_private_key,salt,iv)

# Use the same salt value that was used for encryption (ensure the salt is the same)
# The initialization vector (IV) used during encryption should be the same
def decrypt_private_key(encrypted_private_key: bytes, passphrase: str, salt : bytes, iv : bytes) -> bytes:
    """
    Decrypt an encrypted private key using the passphrase.
    """
    
    # Use PBKDF2 to derive the decryption key from the passphrase
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode())

 

    # Create the AES cipher object for decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the private key
    decrypted_private_key = decryptor.update(encrypted_private_key) + decryptor.finalize()

    return decrypted_private_key




