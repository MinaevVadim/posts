from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from sqlalchemy import select

from log_config import add_logger
from models.users import User
from utils.repository import SQLAlchemyBaseRepository, BaseFollowerRepository


logger = add_logger(__name__)


class SQLAlchemyFollowerRepository(
    SQLAlchemyBaseRepository[User], BaseFollowerRepository
):
    """Repository follower when using SQLAlchemy"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def _helper_get_user(self, username: str) -> User:
        """A method that finds a user in the database by username"""
        stmt = (
            select(self._model)
            .options(selectinload(self._model.following))
            .where(self._model.username == username)  # type: ignore
        )
        result = await self._session.execute(stmt)
        user = result.scalar_one()
        return user

    async def _helper_action_with_follower(
        self, user: User, username: str, action: str
    ) -> bool | None:
        """
        A method that finds a user in the database by name and allows you
        to delete or add a follower to the user
        """
        stmt = select(self._model).where(self._model.username == username)  # type: ignore
        result = await self._session.execute(stmt)
        follower = result.scalars().first()
        method = self._helper_action_with_follower.__name__
        if follower:
            logger.debug(
                "Follower %s was found in a database of the %s function",
                follower.id,
                method,
            )
            if action == "append":
                user.following.append(follower)
            else:
                user.following.remove(follower)
            return True
        logger.debug("Follower was not found in a database of the %s function", method)

    async def add_follower(self, username: str, added_username: str) -> bool | None:
        """The main method of adding a follower"""
        user = await self._helper_get_user(username)
        return await self._helper_action_with_follower(user, added_username, "append")

    async def get_followers(self, idd: int) -> list[User]:
        """
        A method that allows you to get a list of emails of all followers
        of a given user by his ID
        """
        stmt = (
            select(self._model)
            .options(selectinload(self._model.following))
            .where(User.id == idd)  # type: ignore
        )
        user = await self._session.execute(stmt)
        user = user.scalar_one()
        result = [user.email for user in user.following]
        return result

    async def delete_follower(
        self, username: str, removed_username: str
    ) -> bool | None:
        """The main method of removing a follower"""
        user = await self._helper_get_user(username)
        return await self._helper_action_with_follower(user, removed_username, "remove")
