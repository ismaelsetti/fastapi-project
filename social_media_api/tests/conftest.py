import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from social_media_api.routers.post import comment_table, post_table

os.environ["ENV_STATE"] = "test"

from social_media_api.main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> Generator:
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture()
async def async_client(client) -> Generator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
