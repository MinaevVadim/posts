from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar, Generic, Type

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.images import Image
from models.comments import Comment
from models.posts import Post
from models.users import User
from utils.specification import Specification

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T], ABC):
    """The abstract repository class"""

    @abstractmethod
    async def add(self, data: dict) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, name: str) -> T | None:
        raise NotImplementedError()

    @abstractmethod
    async def list(self, specification: Specification) -> Sequence[T]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, idd: int, data: dict) -> T | None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, idd: int) -> bool | None:
        raise NotImplementedError()


class SQLAlchemyBaseRepository(BaseRepository[T], ABC):
    """An abstract repository class using SQLAlchemy"""

    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        self._session: AsyncSession = session
        self._model = model

    async def add(self, data: dict) -> int:
        """Method of adding an object"""
        stmt = insert(self._model).values(**data).returning(self._model.id)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def list(self, specification: Specification) -> Sequence[T]:
        """Method of getting objects"""
        stmt = select(self._model).where(specification.is_satisfied())  # type: ignore
        result = await self._session.execute(stmt)
        result = result.scalars().all()
        return result

    async def get(self, name: str) -> T | None:
        """Method of getting an object"""
        stmt = select(self._model).where(self._model.name == name)  # type: ignore
        result = await self._session.execute(stmt)
        result = result.scalars().first()
        return result

    async def update(self, idd: int, data: dict) -> T | None:
        """Method of updating an object"""
        obj = await self._session.get(self._model, ident=idd)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            return obj

    async def delete(self, idd: int) -> bool | None:
        """Method of removing an object"""
        obj = await self._session.get(self._model, ident=idd)
        if obj:
            await self._session.delete(obj)
            return True


class BaseUserRepository(BaseRepository[User], ABC):
    """An abstract user repository class"""

    async def get_user_by_username(self, username: str) -> User | None:
        raise NotImplementedError()


class BasePostRepository(BaseRepository[Post], ABC):
    """An abstract post repository class"""


class BaseFollowerRepository(BaseRepository[User], ABC):
    """An abstract follower repository class"""

    @abstractmethod
    async def add_follower(self, username: str, added_username: str) -> bool | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_followers(self, idd: int) -> list[User]:
        raise NotImplementedError()

    @abstractmethod
    async def delete_follower(
        self, username: str, removed_username: str
    ) -> bool | None:
        raise NotImplementedError()


class BaseCommentRepository(BaseRepository[Comment], ABC):
    """An abstract comment repository class"""

    @abstractmethod
    async def get_comments(
        self, specification: Specification, idd: int
    ) -> list[Comment]:
        raise NotImplementedError()


class BaseImageRepository(BaseRepository[Image], ABC):
    """An abstract image repository class"""
