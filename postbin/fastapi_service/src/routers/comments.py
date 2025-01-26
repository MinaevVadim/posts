from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from starlette import status

from auth.auth import validate_access_token

from dependencies import comment_service
from log_config import add_logger
from models.users import User
from redis_client import OperationCommentStrategy
from routers.posts import REDIS_CACHE
from schemas.comments import (
    CommentSchema,
    CommentCreateSchema,
    CommentUpdateSchema,
    CommentIDSchema,
    ResultCommentSchema,
)
from services.comments import CommentService

from utils.common import TypeComment

router = APIRouter(prefix="/comments", tags=["comments"])

logger = add_logger(__name__)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CommentSchema])
async def get_comments(
    comments_service: Annotated[CommentService, Depends(comment_service)],
    user: Annotated[User, Depends(validate_access_token)],
    type_name: TypeComment = None,
) -> Sequence[CommentSchema]:
    REDIS_CACHE.strategy = OperationCommentStrategy(
        comments_service, type_name, user.id
    )
    comments = await REDIS_CACHE.commands_cache("comments", type=type_name)
    return comments


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentIDSchema,
)
async def create_comment(
    comments_service: Annotated[CommentService, Depends(comment_service)],
    user: Annotated[User, Depends(validate_access_token)],
    data: CommentCreateSchema,
) -> CommentIDSchema:
    try:
        comment_id = await comments_service.create_comment(data)
    except IntegrityError as exc:
        logger.debug(
            "Author or post does not exist trying create comment was gotten failure %s",
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author or post does not exist.",
        )
    return CommentIDSchema(comment_id=comment_id)


@router.patch(
    "/{idd}",
    status_code=status.HTTP_200_OK,
)
async def change_comment(
    idd: int,
    data: CommentUpdateSchema,
    comments_service: Annotated[CommentService, Depends(comment_service)],
    user: Annotated[User, Depends(validate_access_token)],
) -> dict:
    try:
        comment = await comments_service.change_comment(idd, data)
    except IntegrityError as exc:
        logger.debug(
            "Author does not exist trying change comment was gotten failure %s",
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author does not exist.",
        )
    if comment is None:
        logger.debug("Comment does not exist trying change comment")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment does not exist.",
        )
    return comment


@router.delete(
    "/{idd}",
    status_code=status.HTTP_200_OK,
    response_model=ResultCommentSchema,
)
async def delete_comment(
    idd: int,
    comments_service: Annotated[CommentService, Depends(comment_service)],
    user: Annotated[User, Depends(validate_access_token)],
) -> ResultCommentSchema:
    comment = await comments_service.delete_comment(idd)
    if comment is None:
        logger.debug("Comment does not exist trying delete comment")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment does not exist.",
        )
    return ResultCommentSchema(result=True)
