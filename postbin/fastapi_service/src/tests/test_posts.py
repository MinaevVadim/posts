import os
import sys

import pytest

sys.path.append(os.getcwd())
from tests.factories.factory_boy import session


@pytest.mark.asyncio
async def test_get_posts_status_code_200_and_check_response_content(
    db_client,
    get_access_token,
    post_factory,
    user_factory,
):
    user = user_factory.create()
    await session.commit()
    post_factory.create_batch(2, author_id=user.id)
    await session.commit()
    response = db_client.get("/posts", headers={"Authorization": get_access_token})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Post0"
    assert response.json()[1]["name"] == "Post1"


@pytest.mark.asyncio
async def test_get_posts_status_filtering_status(
    db_client,
    get_access_token,
    post_factory,
    user_factory,
    monkeypatch,
):
    user = user_factory.create()
    await session.commit()
    post = post_factory.create(author_id=user.id)
    await session.commit()
    response = db_client.get(
        f"/posts/?status_name={post.status.lower()}",
        headers={"Authorization": get_access_token},
    )
    assert response.status_code == 200
    assert response.json()[0]["status"] == post.status.lower()


@pytest.mark.asyncio
async def test_get_posts_not_authenticated(db_client):
    response = db_client.get("/posts")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_post_status_201_and_check_response(
    db_client,
    user_factory,
    get_access_token,
):
    user = user_factory.create()
    await session.commit()
    data = {
        "name": "name",
        "content": "content",
        "excerpt": "excerpt",
        "author_id": user.id,
    }
    response = db_client.post(
        "/posts",
        json=data,
        headers={"Authorization": get_access_token},
    )
    assert response.status_code == 201
