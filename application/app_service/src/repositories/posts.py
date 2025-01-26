from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.posts import Post
from utils.repository import SQLAlchemyBaseRepository, BasePostRepository
from utils.specification import Specification


class SQLAlchemyPostRepository(SQLAlchemyBaseRepository[Post], BasePostRepository):
    """Repository post when using SQLAlchemy"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Post)

    async def list(self, specification: Specification) -> Sequence[Post]:
        """Method for getting a list of posts"""
        stmt = (
            select(self._model)
            .options(selectinload(self._model.images))
            .where(specification.is_satisfied())  # type: ignore
        )
        result = await self._session.execute(stmt)
        posts = result.scalars().all()
        result = [post.to_dict() for post in posts]
        return result
