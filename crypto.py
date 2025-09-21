import base64
import os
import json
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

PBKDF2_ITERATIONS = 390000
SALT_LEN = 16
MAGIC = b"STEG"

def _derive_fernet_key(pass_id: str, salt: bytes) -> bytes:
    try:
        algorithm = hashes.SHA256()
        # Test if SHA256 is supported
        _ = algorithm.name
    except Exception:
        algorithm = hashes.SHA1()  # Fallback if SHA256 fails

    kdf = PBKDF2HMAC(
        algorithm=algorithm,
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    key = kdf.derive(pass_id.encode("utf-8"))
    return base64.urlsafe_b64encode(key)

def encrypt_payload(message: str, pass_id: str, metadata: dict = None) -> bytes:
    salt = os.urandom(SALT_LEN)
    fernet_key = _derive_fernet_key(pass_id, salt)

    payload = {
        "message": message,
        "metadata": metadata or {}
    }
    json_data = json.dumps(payload).encode("utf-8")
    token = Fernet(fernet_key).encrypt(json_data)

    core = salt + token
    length_bytes = len(core).to_bytes(4, "big")
    return MAGIC + length_bytes + core

def decrypt_payload(payload: bytes, pass_id: str) -> str:
    if len(payload) < 8 or payload[:4] != MAGIC:
        raise ValueError("Invalid or corrupted payload format.")

    total_len = int.from_bytes(payload[4:8], "big")
    core = payload[8:8+total_len]

    if len(core) < SALT_LEN + 1:
        raise ValueError("Incomplete payload data.")

    salt = core[:SALT_LEN]
    token = core[SALT_LEN:]
    fernet_key = _derive_fernet_key(pass_id, salt)

    try:
        decrypted = Fernet(fernet_key).decrypt(token)
        return decrypted.decode("utf-8")
    except InvalidToken:
        raise ValueError("Incorrect pass ID or corrupted data.")
