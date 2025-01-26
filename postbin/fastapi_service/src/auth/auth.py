from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from jwt import InvalidTokenError
from starlette import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from auth.utils import validate_password, decode_jwt
from dependencies import user_service
from log_config import add_logger
from models.users import User
from schemas.users import UserCreateSchema
from services.users import UserService

logger = add_logger(__name__)

http_bearer = HTTPBearer()


async def validate_auth_user(
    data: UserCreateSchema,
    user_services: Annotated[UserService, Depends(user_service)],
) -> User:
    """Verifying the validity of user authentication"""
    user = await user_services.get_user(data.username)
    un_authed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    func = validate_auth_user.__name__
    if user is None:
        logger.debug(
            "User %s was not found in a database of the %s function during validation",
            data.username,
            func,
        )
        raise un_authed_exc
    if user.username != data.username:
        logger.debug(
            "Invalid username %s during validation in %s function",
            data.username,
            func,
        )
        raise un_authed_exc
    if not validate_password(data.password, user.password):
        logger.debug(
            "Invalid password %s during validation in %s function",
            data.password,
            func,
        )
        raise un_authed_exc
    logger.debug(
        "User with %s id was found in a database and checked"
        " during validation of the %s function",
        user.id,
        func,
    )
    return user


async def check_token_type(payload: dict, token_type: str) -> bool:
    """Checking the user's token type"""
    if payload.get(TOKEN_TYPE_FIELD) != token_type:
        logger.debug("Invalid token type was gotten %s", payload.get(TOKEN_TYPE_FIELD))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type."
        )
    return True


async def check_valid_token(token: str) -> dict:
    """Checking the validity of the token"""
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as exc:
        logger.debug("Token is not valid was gotten failure %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is not valid.",
        )
    return payload


async def get_user_payload(payload: dict, user_services: UserService) -> User:
    """Checking the user's existence in the database when comparing data from the jwt token"""
    user = await user_services.get_user(payload.get("username"))
    if user is None:
        logger.debug("User is not found was gotten %s", payload.get("username"))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not found",
        )
    return user


async def validate_access_token(
    user_services: Annotated[UserService, Depends(user_service)],
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User:
    """Access token verification"""
    token = credentials.credentials
    payload = await check_valid_token(token)
    if await check_token_type(payload, ACCESS_TOKEN_TYPE):
        user = await get_user_payload(payload, user_services)
        return user


async def validate_refresh_token(
    user_services: Annotated[UserService, Depends(user_service)],
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User:
    """Checking the refresh token"""
    token = credentials.credentials
    payload = await check_valid_token(token)
    if await check_token_type(payload, REFRESH_TOKEN_TYPE):
        user = await get_user_payload(payload, user_services)
        return user
