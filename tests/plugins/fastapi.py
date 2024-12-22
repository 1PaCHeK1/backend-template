from collections.abc import AsyncIterator

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI

from app.adapters.api.app import create_app

app = create_app()


@pytest.fixture
async def fastapi_app() -> AsyncIterator[FastAPI]:
    async with LifespanManager(app=app):
        yield app


@pytest.fixture
def app_transport(fastapi_app: FastAPI) -> httpx.AsyncBaseTransport:
    return httpx.ASGITransport(app=fastapi_app)


@pytest.fixture
async def http_client(
    app_transport: httpx.AsyncBaseTransport,
) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        transport=app_transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
async def authenticated_http_client(
    app_transport: httpx.AsyncBaseTransport,
    access_token: str,
    _autouse_keycloack_mock: None,
) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        base_url="http://test",
        transport=app_transport,
        headers={"Authorization": f"Bearer {access_token}"},
    ) as client:
        yield client
