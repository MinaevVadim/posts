from typing import Annotated

import aioredis
from fastapi import APIRouter, Depends, HTTPException, File, Body, UploadFile
from sqlalchemy.exc import IntegrityError

from starlette import status

from auth.auth import validate_access_token
from communication.media import CommunicateClient

from dependencies import post_service, follower_service, image_service
from env_config import settings
from log_config import add_logger
from models.users import User
from redis_client import RedisCache, OperationPostStrategy
from schemas.images import ImageSchema
from schemas.posts import (
    PostCreateSchema,
    PostSchema,
    PostUpdateSchema,
    IDPostSchema,
    ResultPostSchema,
)
from services.followers import FollowerService
from services.images import ImageService
from services.posts import PostService
from utils.common import Status

router = APIRouter(prefix="/posts", tags=["posts"])

REDIS = aioredis.from_url(f"redis://{settings.redis.redis_host}")
REDIS_CACHE = RedisCache(REDIS, 30)

logger = add_logger(__name__)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[PostSchema],
)
async def get_posts(
    posts_service: Annotated[PostService, Depends(post_service)],
    user: Annotated[User, Depends(validate_access_token)],
    status_name: Status = None,
) -> list[PostSchema]:
    REDIS_CACHE.strategy = OperationPostStrategy(posts_service, status_name)
    posts = await REDIS_CACHE.commands_cache("posts", status=status_name)
    return posts


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IDPostSchema,
)
async def create_post(
    posts_service: Annotated[PostService, Depends(post_service)],
    user: Annotated[User, Depends(validate_access_token)],
    followers_service: Annotated[FollowerService, Depends(follower_service)],
    images_service: Annotated[ImageService, Depends(image_service)],
    data: PostCreateSchema = Body(...),
    file: Annotated[
        UploadFile, File(description="This file reads as UploadFile")
    ] = None,
) -> IDPostSchema:
    try:
        post_id = await posts_service.create_post_and_send_email(
            data,
            user.id,
            followers_service,
        )
        link_image = await CommunicateClient().send_image(file, post_id)
        if link_image:
            data = ImageSchema(image=link_image, post_id=post_id)
            await images_service.create_image(data)
    except IntegrityError as exc:
        logger.debug(
            "Author does not exist trying create post was gotten failure %s",
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author does not exist.",
        )
    return IDPostSchema(post_id=post_id)


@router.patch(
    "/{idd}",
    status_code=status.HTTP_200_OK,
)
async def change_post(
    idd: int,
    data: PostUpdateSchema,
    posts_service: Annotated[PostService, Depends(post_service)],
    user: Annotated[User, Depends(validate_access_token)],
) -> dict:
    try:
        post = await posts_service.change_post(idd, data)
    except IntegrityError as exc:
        logger.debug(
            "Author does not exist trying change post was gotten failure %s",
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author does not exist.",
        )
    if post is None:
        logger.debug("Post does not exist trying change post")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post does not exist.",
        )
    return post


@router.delete(
    "/{idd}",
    status_code=status.HTTP_200_OK,
    response_model=ResultPostSchema,
)
async def delete_post(
    idd: int,
    posts_service: Annotated[PostService, Depends(post_service)],
    user: Annotated[User, Depends(validate_access_token)],
) -> ResultPostSchema:
    post = await posts_service.delete_post(idd)
    if post is None:
        logger.debug("Post does not exist trying delete post")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post does not exist.",
        )
    return ResultPostSchema(result=True)
