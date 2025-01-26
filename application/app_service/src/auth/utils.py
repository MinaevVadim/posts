import datetime
from datetime import timedelta

import bcrypt
import jwt

from env_config import settings


def encode_jwt(
    payload: dict,
    private_key=settings.auth_jwt.private_key_path.read_text(),
    algorithm=settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """Creating and setting jwt token time parameters"""
    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    return jwt.encode(to_encode, private_key, algorithm)


def decode_jwt(
    token: str | bytes,
    public_key=settings.auth_jwt.public_key_path.read_text(),
    algorithm=settings.auth_jwt.algorithm,
) -> dict:
    """Decryption of the jwt token"""
    return jwt.decode(token, public_key, algorithm)


def hash_password(password: str) -> bytes:
    """Encrypting the user's password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    """Decryption of the user's password"""
    return bcrypt.checkpw(password.encode(), hashed_password)
