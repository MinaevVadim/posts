from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from sqlalchemy import insert
from utils.repository import SQLAlchemyBaseRepository, BaseUserRepository
from sqlalchemy import select
from auth.utils import hash_password


class SQLAlchemyUserRepository(SQLAlchemyBaseRepository[User], BaseUserRepository):
    """Repository user when using SQLAlchemy"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def add(self, data: dict) -> int:
        """The method of adding a user"""
        stmt = (
            insert(self._model)
            .values(
                username=data["username"],
                password=hash_password(data["password"]),
                email=data["email"],
            )
            .returning(self._model.id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def get(self, name: str) -> User | None:
        """User acquisition method"""
        stmt = select(self._model).where(self._model.username == name)  # type: ignore
        result = await self._session.execute(stmt)
        result = result.scalars().first()
        return result
