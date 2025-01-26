from typing import Annotated, AsyncGenerator, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_config import async_session
from services.comments import CommentService
from services.followers import FollowerService
from services.images import ImageService
from services.posts import PostService
from services.users import UserService


async def db():
    async with async_session() as session:
        yield session


def post_service(
    session: Annotated[AsyncGenerator[AsyncSession, Any], Depends(db)]
) -> PostService:
    """A function that performs the logic of the post service"""
    return PostService(session)


def user_service(
    session: Annotated[AsyncGenerator[AsyncSession, Any], Depends(db)]
) -> UserService:
    """A function that performs the logic of the user service"""
    return UserService(session)


def follower_service(
    session: Annotated[AsyncGenerator[AsyncSession, Any], Depends(db)]
) -> FollowerService:
    """A function that performs the logic of the follower service"""
    return FollowerService(session)


def comment_service(
    session: Annotated[AsyncGenerator[AsyncSession, Any], Depends(db)]
) -> CommentService:
    """A function that performs the logic of the comment service"""
    return CommentService(session)


def image_service(
    session: Annotated[AsyncGenerator[AsyncSession, Any], Depends(db)]
) -> ImageService:
    """A function that performs the logic of the image service"""
    return ImageService(session)
