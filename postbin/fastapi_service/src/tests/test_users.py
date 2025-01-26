import os
import sys

import pytest

sys.path.append(os.getcwd())
from tests.factories.factory_boy import session


@pytest.mark.asyncio
async def test_user_login_status_code_201_and_existing_of_token(
    db_client, user_factory
):
    user = user_factory.create()
    await session.commit()
    dct_user = {
        "username": user.username,
        "password": "password",
        "email": user.email,
    }
    response = db_client.post("/auth/login", json=dct_user)
    assert response.status_code == 201
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None
    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_user_login_status_code_422_failed(db_client):
    dct_user = {
        "username": "fake_username",
        "password": "fake_password",
        "email": "fake_email",
    }
    response = db_client.post("/auth/login", json=dct_user)
    assert response.status_code == 422
    assert "value is not a valid email address" in response.json()["detail"][0]["msg"]


@pytest.mark.asyncio
async def test_user_login_status_code_401_failed(db_client):
    dct_user = {
        "username": "fake_username",
        "password": "fake_password",
        "email": "fake@gmail.com",
    }
    response = db_client.post("/auth/login", json=dct_user)
    assert response.status_code == 401
    assert response.json()["detail"] == "invalid username or password"


@pytest.mark.asyncio
async def test_user_register_status_code_201_and_existing_of_user(db_client):
    dct_user = {
        "username": "username",
        "password": "password",
        "email": "user@gmail.com",
    }
    response = db_client.post("/auth/register", json=dct_user)
    assert response.status_code == 201
    assert response.json() == {"user_id": 1}


@pytest.mark.parametrize(
    "email, username, password, status_code",
    (
        ("user@gmail.com", "user", "password", 201),
        ("gmail", "user", "password", 422),
        ("user@gmail.com", 888, "password", 422),
        ("user@gmail.com", "user", 888, 422),
    ),
)
@pytest.mark.asyncio
async def test_user_register_different_status_codes(
    db_client,
    email,
    username,
    password,
    status_code,
):
    dct_user = {
        "username": username,
        "password": password,
        "email": email,
    }
    response = db_client.post("/auth/register", json=dct_user)
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_user_refresh_token_status_code_201_and_existing_token(
    db_client, user_factory
):
    user = user_factory.create()
    await session.commit()
    dct_user = {
        "username": user.username,
        "password": "password",
        "email": user.email,
    }
    response = db_client.post("/auth/login", json=dct_user)
    refresh_token = response.json()["refresh_token"]

    response = db_client.get(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert response.status_code == 201


@pytest.mark.parametrize(
    "auth, status_code",
    (
        ({"Authorization": f"Bearer 00000"}, 401),
        (None, 403),
    ),
)
@pytest.mark.asyncio
async def test_user_refresh_token_not_authenticated_and_forbidden(
    db_client,
    auth,
    status_code,
):
    response = db_client.get("/auth/refresh", headers=auth)
    assert response.status_code == status_code
