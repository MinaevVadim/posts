from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.comments import Comment
from utils.repository import SQLAlchemyBaseRepository, BaseCommentRepository
from utils.specification import Specification


class SQLAlchemyCommentRepository(
    SQLAlchemyBaseRepository[Comment], BaseCommentRepository
):
    """Repository comment when using SQLAlchemy"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Comment)

    async def get_comments(
        self, specification: Specification, idd: int
    ) -> list[Comment]:
        """Getting comments on the author's ID"""
        stmt = select(self._model).where(
            specification.is_satisfied(), self._model.author_id == idd  # type: ignore
        )
        result = await self._session.execute(stmt)
        result = result.scalars().all()
        return list(result)
