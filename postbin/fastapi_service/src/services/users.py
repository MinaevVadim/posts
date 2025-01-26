from typing import AsyncGenerator

from log_config import add_logger, logged
from models.users import User
from schemas.users import UserCreateSchema
from unit_of_work.utils import UserUnitOfWork

logger = add_logger(__name__)


@logged(logger)
class UserService:
    """A class that allows you to work with users"""

    def __init__(self, session: AsyncGenerator) -> None:
        self.session = session

    async def create_user(self, user: UserCreateSchema) -> int:
        """User creation method"""
        user_dict = user.model_dump()
        async with UserUnitOfWork(session_factory=self.session) as uow:
            user_id = await uow.users.add(user_dict)
            await uow.commit()
            return user_id

    async def get_user(self, name: str) -> User | None:
        """Method of receiving a one user"""
        async with UserUnitOfWork(session_factory=self.session) as uow:
            user = await uow.users.get(name)
            return user
