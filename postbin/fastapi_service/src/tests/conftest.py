import asyncio
import os
import sys


import pytest_asyncio
from pytest_factoryboy import register
import pytest
from starlette.testclient import TestClient

sys.path.append(os.getcwd())
from dependencies import db

from models import Base


from main import app
from tests.factories.factory_boy import (
    UserFactory,
    engine,
    session,
    PostFactory,
    CommentFactory,
    ImageFactory,
)

register(UserFactory)
register(PostFactory)
register(CommentFactory)
register(ImageFactory)


async def create_and_drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def override():
        async with session() as session_for_override:
            async with session_for_override.begin():
                yield session_for_override

    app.dependency_overrides[db] = override


@pytest.fixture(scope="session", autouse=True)
def db_create():
    asyncio.run(create_and_drop_tables())
    yield


async def clean_tables():
    for tbl in reversed(Base.metadata.sorted_tables):
        await session.execute(tbl.delete())
        await session.commit()


@pytest.fixture
def db_client():
    client = TestClient(app)
    yield client
    asyncio.run(clean_tables())


@pytest_asyncio.fixture
async def get_access_token(db_client, user_factory):
    user = user_factory.create()
    await session.commit()
    dct_user = {
        "username": user.username,
        "password": "password",
        "email": user.email,
    }
    response = db_client.post("/auth/login", json=dct_user)
    return f"Bearer {response.json()['access_token']}"
