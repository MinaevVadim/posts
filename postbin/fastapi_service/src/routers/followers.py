from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from starlette import status

from auth.auth import validate_access_token
from dependencies import follower_service
from log_config import add_logger
from models.users import User
from schemas.users import ResultFollowerSchema
from services.followers import FollowerService

router = APIRouter(prefix="/followers", tags=["followers"])

logger = add_logger(__name__)


@router.post(
    "/{name}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResultFollowerSchema,
)
async def create_follower(
    name: str,
    user: Annotated[User, Depends(validate_access_token)],
    followers_service: Annotated[FollowerService, Depends(follower_service)],
) -> ResultFollowerSchema:
    try:
        follower = await followers_service.add_follower(user.username, name)
    except IntegrityError as exc:
        logger.debug(
            "This user is already on the list of followers trying create follower was gotten failure %s",
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is already on the list of followers.",
        )
    if follower is None:
        logger.debug("Follower does not exist trying create follower")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Follower does not exist.",
        )
    return ResultFollowerSchema(result=True)


@router.delete(
    "/{name}",
    status_code=status.HTTP_200_OK,
    response_model=ResultFollowerSchema,
)
async def remove_follower(
    name: str,
    user: Annotated[User, Depends(validate_access_token)],
    followers_service: Annotated[FollowerService, Depends(follower_service)],
) -> ResultFollowerSchema:
    try:
        follower = await followers_service.delete_follower(user.username, name)
    except ValueError as exc:
        logger.debug(
            "This user is not on the list of followers"
            " trying create follower was gotten failure %s",
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is not on the list of followers.",
        )
    if follower is None:
        logger.debug("Follower does not exist trying remove follower")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Follower does not exist.",
        )
    return ResultFollowerSchema(result=True)
