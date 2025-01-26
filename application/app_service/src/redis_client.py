import pickle
from abc import ABC, abstractmethod
from typing import TypeVar

from aioredis import Redis

from services.comments import CommentService
from services.posts import PostService
from utils.common import TypeComment, Status
from utils.specification import IsTypeSpecification, IsStatusSpecification


T = TypeVar("T")


class BaseOperationStrategy(ABC):
    """An abstract class that allows you to Interchangeably perform various operations"""

    @abstractmethod
    async def operation(self) -> T:
        raise NotImplementedError()


class OperationCommentStrategy(BaseOperationStrategy):
    """A class that allows you to get a list of comments"""

    def __init__(
        self, service: CommentService, type_name: TypeComment, user_id: int
    ) -> None:
        self.type_name = type_name
        self.user_id = user_id
        self.service = service

    async def operation(self) -> T:
        """Method of receiving comments"""
        return await self.service.get_comments(
            IsTypeSpecification(self.type_name), self.user_id
        )


class OperationPostStrategy(BaseOperationStrategy):
    """A class that allows you to get a list of posts"""

    def __init__(self, service: PostService, status_name: Status) -> None:
        self.status_name = status_name
        self.service = service

    async def operation(self) -> T:
        """Method of receiving posts"""
        return await self.service.get_posts(IsStatusSpecification(self.status_name))


class RedisCache:
    """Caching class using radis using different operations"""

    def __init__(self, redis_cli: Redis, time: int) -> None:
        self.redis = redis_cli
        self._strategy = None
        self.time = time

    @property
    def strategy(self) -> BaseOperationStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BaseOperationStrategy) -> None:
        self._strategy = strategy

    async def commands_cache(self, key: str, **kwargs) -> T:
        """The method of caching various data"""
        cache_bytes = await self.redis.get(key + "".join(kwargs))
        if cache_bytes:
            cache = pickle.loads(cache_bytes)
            result = cache
        else:
            result = await self.strategy.operation()
            cache_bytes = pickle.dumps(result)
            await self.redis.set(key, cache_bytes, self.time)
        return result
