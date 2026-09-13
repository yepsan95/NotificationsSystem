import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

password_context = PasswordHash.recommended()

PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY", "").replace("\\n", "\n")
PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY", "").replace("\\n", "\n")

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRATION_TIME_IN_MINUTES = 15
REFRESH_TOKEN_EXPIRATION_TIME_IN_DAYS = 7


def hash_password(password: str) -> str:
    """
    Hashes password with Argon2id algorithm.
    """

    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain against hashed password.
    """

    return password_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    """
    Creates JWT Access Token with assymetric encryption RS256 using private key.
    """

    expiration_unix_timestamp = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRATION_TIME_IN_MINUTES
    )
    to_encode = {"exp": expiration_unix_timestamp, "sub": subject}

    return jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decodes and validates JWT Access Token with RS256 using public key.
    """

    return jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])


def generate_refresh_token() -> str:
    """
    Generates cryptographically safe opaque random character token.
    """

    return secrets.token_urlsafe(64)
