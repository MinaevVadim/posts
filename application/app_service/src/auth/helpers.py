from datetime import timedelta

from auth.utils import encode_jwt
from env_config import settings
from schemas.users import UserSchema


TOKEN_TYPE_FIELD: str = "type"
ACCESS_TOKEN_TYPE: str = "access"
REFRESH_TOKEN_TYPE: str = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """Creating a jwt token"""
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserSchema) -> str:
    """Creating a jwt access token"""
    payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: UserSchema) -> str:
    """Creating a jwt refresh token"""
    payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
