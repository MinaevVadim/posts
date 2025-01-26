import json
from typing import Sequence, AsyncGenerator

from config import RabbitMQClient
from env_config import settings
from log_config import add_logger, logged
from models.posts import Post
from schemas.posts import PostCreateSchema
from unit_of_work.utils import PostUnitOfWork
from utils.specification import Specification

logger = add_logger(__name__)


@logged(logger)
class PostService:
    """A class that allows you to work with post"""

    def __init__(self, session: AsyncGenerator) -> None:
        self.session = session

    async def create_post_and_send_email(
        self,
        post: PostCreateSchema,
        user_id: int,
        followers_service,
    ) -> int:
        """The method of creating a post and sending data to the notification service"""
        post_dict = post.model_dump()
        async with PostUnitOfWork(session_factory=self.session) as uow:
            post_id = await uow.posts.add(post_dict)
            await uow.commit()
        followers_emails = await followers_service.get_followers(user_id)
        data = {"user_id": user_id, "post_id": post_id, "emails": followers_emails}
        await self._send_email(json.dumps(data))
        return post_id

    async def get_posts(self, specification: Specification) -> Sequence[Post]:
        """Method of receiving posts"""
        async with PostUnitOfWork(session_factory=self.session) as uow:
            posts = await uow.posts.list(specification)
            return posts

    async def change_post(self, idd: int, post: PostCreateSchema) -> Post | None:
        """Method of changing post"""
        post_dict = post.model_dump(exclude_none=True)
        async with PostUnitOfWork(session_factory=self.session) as uow:
            post = await uow.posts.update(idd, post_dict)
            await uow.commit()
            return post

    async def delete_post(self, idd: int) -> bool | None:
        """Method of removing post"""
        async with PostUnitOfWork(session_factory=self.session) as uow:
            result = await uow.posts.delete(idd)
            await uow.commit()
            return result

    @classmethod
    async def _send_email(cls, body: str | bytes) -> None:
        """
        A method of sending data to a media service to notify followers of the
        creation of a new post
        """
        client = RabbitMQClient(
            host=settings.rabbitmq_host, port=settings.rabbitmq_port
        )
        client.public_basic(queue="email", exchange="", route_key="email", body=body)
