from abc import ABC, abstractmethod

from db.db_config import async_session
from repositories.comments import SQLAlchemyCommentRepository
from repositories.followers import SQLAlchemyFollowerRepository
from repositories.images import SQLAlchemyImageRepository
from repositories.posts import SQLAlchemyPostRepository
from repositories.users import SQLAlchemyUserRepository
from utils.repository import (
    BaseUserRepository,
    BasePostRepository,
    BaseFollowerRepository,
    BaseCommentRepository,
    BaseImageRepository,
)


class BaseUnitOfWork(ABC):
    """
    An abstract unit of work class for the atomicity of operations
    across multiple repositories
    """

    async def __aenter__(self) -> "":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError()


class SQLAlchemyBaseUnitOfWork(BaseUnitOfWork):
    """
    A unit of work class for the atomicity of operations
    across multiple repositories with SQLAlchemy
    """

    def __init__(self, session_factory: async_session) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> "":
        self._session = self._session_factory
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        self._session.expunge_all()
        await self._session.rollback()


class UserUnitOfWork(SQLAlchemyBaseUnitOfWork):
    """
    A unit of work class for users operations with SQLAlchemy
    """

    async def __aenter__(self) -> "":
        uow = await super().__aenter__()
        self.users: BaseUserRepository = SQLAlchemyUserRepository(session=self._session)
        return uow


class PostUnitOfWork(SQLAlchemyBaseUnitOfWork):
    """
    A unit of work class for posts operations with SQLAlchemy
    """

    async def __aenter__(self) -> "":
        uow = await super().__aenter__()
        self.posts: BasePostRepository = SQLAlchemyPostRepository(session=self._session)
        return uow


class FollowerUnitOfWork(SQLAlchemyBaseUnitOfWork):
    """
    A unit of work class for followers operations with SQLAlchemy
    """

    async def __aenter__(self) -> "":
        uow = await super().__aenter__()
        self.followers: BaseFollowerRepository = SQLAlchemyFollowerRepository(
            session=self._session
        )
        return uow


class CommentUnitOfWork(SQLAlchemyBaseUnitOfWork):
    """
    A unit of work class for comments operations with SQLAlchemy
    """

    async def __aenter__(self) -> "":
        uow = await super().__aenter__()
        self.comments: BaseCommentRepository = SQLAlchemyCommentRepository(
            session=self._session
        )
        return uow


class ImageUnitOfWork(SQLAlchemyBaseUnitOfWork):
    """
    A unit of work class for images operations with SQLAlchemy
    """

    async def __aenter__(self) -> "":
        uow = await super().__aenter__()
        self.images: BaseImageRepository = SQLAlchemyImageRepository(
            session=self._session
        )
        return uow
