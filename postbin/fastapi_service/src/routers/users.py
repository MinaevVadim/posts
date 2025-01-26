from typing import Annotated

from fastapi import APIRouter, Depends, requests

from starlette import status

from auth.auth import validate_auth_user, validate_refresh_token
from auth.helpers import create_access_token, create_refresh_token
from dependencies import user_service
from models.users import User
from schemas.tokens import TokenSchema
from schemas.users import UserCreateSchema, IDUserSchema
from services.users import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=IDUserSchema,
)
async def register_user(
    data: UserCreateSchema,
    users_service: Annotated[UserService, Depends(user_service)],
) -> IDUserSchema:
    user_id = await users_service.create_user(data)
    return IDUserSchema(user_id=user_id)


@router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenSchema,
)
async def login_user(
    user: Annotated[validate_auth_user, Depends(validate_auth_user)]
) -> TokenSchema:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get(
    "/refresh",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenSchema,
    response_model_exclude_none=True,
)
async def get_refresh_token(
    user: Annotated[User, Depends(validate_refresh_token)]
) -> TokenSchema:
    access_token = create_access_token(user)
    return TokenSchema(access_token=access_token)
