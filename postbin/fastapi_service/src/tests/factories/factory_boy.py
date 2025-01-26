from asyncio import current_task

import factory
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    async_scoped_session,
)

from auth.utils import hash_password
from models.posts import Post
from models.users import User
from models.comments import Comment
from models.images import Image
from env_config import settings
from utils.common import Status, StatusComment, TypePost, TypeComment

user = settings.postgres_user
pwd = settings.postgres_password
host = settings.postgres_host
port = settings.postgres_port


class MyEngine:
    def __init__(self) -> None:
        self.path = f"postgresql+asyncpg://{user}:{pwd}@{host}:{port}/test"
        self.engine = create_async_engine(
            self.path,
            poolclass=NullPool,
        )

    def async_session(self):
        return async_scoped_session(
            async_sessionmaker(
                self.engine,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )


my_engine = MyEngine()
engine = my_engine.engine
session = my_engine.async_session()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n + 1)
    username = factory.Sequence(lambda n: "User%d" % n)
    password = hash_password("password")
    email = factory.LazyAttribute(lambda x: "%s@mail.com" % x.username)


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: "Post%d" % n)
    content = factory.Faker("sentence", nb_words=10)
    excerpt = factory.Faker("sentence", nb_words=10)
    status = factory.Faker("random_element", elements=[x.name for x in Status])
    status_comment = factory.Faker(
        "random_element", elements=[x.name for x in StatusComment]
    )
    type = factory.Faker("random_element", elements=[x.name for x in TypePost])
    comment_count = factory.Faker("random_number")

    author_id = factory.SubFactory(UserFactory)


class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Comment
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n + 1)
    karma = factory.Faker("random_number")
    content = factory.Faker("sentence", nb_words=10)
    approved = True
    type = factory.Faker("random_element", elements=[x.value for x in TypeComment])
    comment_count = factory.Faker("random_number")

    author_id = factory.SubFactory(UserFactory)
    post_id = factory.SubFactory(PostFactory)


class ImageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Image
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n + 1)
    image = factory.Faker("sentence", nb_words=20)

    post_id = factory.SubFactory(PostFactory)
