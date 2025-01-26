from typing import AsyncGenerator

from log_config import add_logger, logged
from models.users import User
from unit_of_work.utils import FollowerUnitOfWork


logger = add_logger(__name__)


@logged(logger)
class FollowerService:
    """A class that allows you to work with follower"""

    def __init__(self, session: AsyncGenerator) -> None:
        self.session = session

    async def add_follower(self, username: str, added_username: str) -> None:
        """Method of adding a new follower"""
        async with FollowerUnitOfWork(session_factory=self.session) as uow:
            follower = await uow.followers.add_follower(username, added_username)
            await uow.commit()
            return follower

    async def get_followers(self, idd: int) -> list[User]:
        """Method of receiving followers"""
        async with FollowerUnitOfWork(session_factory=self.session) as uow:
            followers = await uow.followers.get_followers(idd)
            return followers

    async def delete_follower(self, username: str, remove_username: str) -> bool | None:
        """Method of deleting a follower"""
        async with FollowerUnitOfWork(session_factory=self.session) as uow:
            follower = await uow.followers.delete_follower(username, remove_username)
            await uow.commit()
            return follower
