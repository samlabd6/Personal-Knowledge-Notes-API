import hashlib
import os

# Simple password hashing and verification using SHA-256 with a random salt.
def hash_password(pw):
    salt = os.urandom(16)
    return salt.hex(), hashlib.sha256(salt + pw.encode()).hexdigest()

# get the stored salt and hash from the database, then verify against the provided password
def verify_password(stored_salt, stored_hash, provided_password):
    salt_bytes = bytes.fromhex(stored_salt)
    if stored_hash == hashlib.sha256(salt_bytes + provided_password.encode()).hexdigest():
        return True
    return False


