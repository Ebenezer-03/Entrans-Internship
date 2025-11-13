import os
import hashlib
import base64
from hmac import compare_digest

ITERATIONS = 200_000
SALT_BYTES = 16
HASH_NAME = "sha256"


def hash_password(plain: str) -> str:
    """Return a string containing salt and hash, safe to store."""
    salt = os.urandom(SALT_BYTES)
    dk = hashlib.pbkdf2_hmac(HASH_NAME, plain.encode("utf-8"), salt, ITERATIONS)
    return f"{base64.b64encode(salt).decode()}${base64.b64encode(dk).decode()}"


def verify_password(plain: str, stored: str) -> bool:
    """Verify a plaintext password against stored salt$hash form."""
    try:
        salt_b64, dk_b64 = stored.split("$")
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(dk_b64)

        test = hashlib.pbkdf2_hmac(HASH_NAME, plain.encode("utf-8"), salt, ITERATIONS)

        # FIX: use hmac.compare_digest (works in all Python versions)
        return compare_digest(test, expected)

    except Exception:
        return False
