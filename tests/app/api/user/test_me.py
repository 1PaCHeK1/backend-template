from http import HTTPStatus

import httpx
import pytest
from fastapi import FastAPI

from app.connectors.keycloak.dto import DecodedTokenDTO

pytestmark = [pytest.mark.anyio]


@pytest.fixture
def endpoint_url(fastapi_app: FastAPI) -> str:
    return fastapi_app.url_path_for("user_me")


async def test_should_be_authenticated(
    endpoint_url: str,
    http_client: httpx.AsyncClient,
) -> None:
    response = await http_client.get(endpoint_url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_ok(
    endpoint_url: str,
    authenticated_http_client: httpx.AsyncClient,
    access_token_dto: DecodedTokenDTO,
) -> None:
    response = await authenticated_http_client.get(endpoint_url)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == str(access_token_dto.sub)
