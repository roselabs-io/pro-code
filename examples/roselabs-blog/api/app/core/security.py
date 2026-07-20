import datetime as dt

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from app.core.config import settings

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return _hasher.verify(password_hash, password)
    except VerificationError:
        return False


def create_access_token(subject: str) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + dt.timedelta(seconds=settings.access_token_ttl_seconds),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
