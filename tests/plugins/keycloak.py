import time
import uuid
from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import MagicMock, Mock

import aioinject
import jwt
import pytest
from aioinject.testing import TestContainer
from result import Ok

from app.connectors.keycloak.dto import DecodedTokenDTO
from app.connectors.keycloak.service import KeycloakService
from app.connectors.keycloak.settings import KeycloakSettings
from lib.settings import get_settings
from tests.settings import TestSettings


@pytest.fixture(scope="session")
def keycloak_user_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture(scope="session")
def jwt_payload() -> dict[str, Any]:
    current_timestamp = int(time.time())
    return {
        "exp": current_timestamp + 900,
        "iat": current_timestamp,
        "auth_time": current_timestamp,
        "jti": str(uuid.uuid4()),
        "iss": "https://kc.domain.site/realms/test",
        "aud": [
            "fastapi-auth-test",
            "auth-backend",
            "realm-management",
            "-auth-test2",
            "security-admin-console",
            "miscloak",
            "broker",
            "-auth-test",
            "account",
        ],
        "sub": str(uuid.uuid4()),
        "typ": "Bearer",
        "azp": "fastapi-auth-test",
        "session_state": str(uuid.uuid4()),
        "acr": "0",
        "allowed-origins": ["/*"],
        "realm_access": {
            "roles": [
                "offline_access",
                "view-users",
                "uma_authorization",
            ],
        },
        "resource_access": {
            "realm-management": {
                "roles": [
                    "view-realm",
                    "view-identity-providers",
                    "manage-identity-providers",
                    "impersonation",
                    "realm-admin",
                    "create-client",
                    "manage-users",
                    "query-realms",
                    "view-authorization",
                    "query-clients",
                    "query-users",
                    "manage-events",
                    "manage-realm",
                    "view-events",
                    "view-users",
                    "view-clients",
                    "manage-authorization",
                    "manage-clients",
                    "query-groups",
                ],
            },
            "-auth-test2": {"roles": ["uma_protection"]},
            "auth-backend": {"roles": ["uma_protection"]},
            "security-admin-console": {"roles": ["uma_protection"]},
            "miscloak": {"roles": ["uma_protection"]},
            "broker": {"roles": ["read-token"]},
            "account": {
                "roles": [
                    "manage-account",
                    "view-applications",
                    "view-consent",
                    "view-groups",
                    "manage-account-links",
                    "delete-account",
                    "manage-consent",
                    "view-profile",
                ],
            },
        },
        "scope": "fastapi_auth_test_scope email backend profile",
        "sid": str(uuid.uuid4()),
        "email_verified": True,
        "name": "test test",
        "groups": [
            "offline_access",
            "view-users",
            "uma_authorization",
            "offline_access",
            "view-users",
            "uma_authorization",
        ],
        "preferred_username": "test",
        "given_name": "test",
        "family_name": "test",
        "email": "test@domain.ru",
    }


@pytest.fixture(scope="session")
async def access_token_dto(
    jwt_payload: dict[str, Any],
    keycloak_user_id: uuid.UUID,
) -> DecodedTokenDTO:
    current_timestamp = int(time.time())

    payload = dict(jwt_payload)
    payload["exp"] = current_timestamp + 900
    payload["iat"] = current_timestamp
    payload["auth_time"] = current_timestamp
    payload["sub"] = str(keycloak_user_id)
    return DecodedTokenDTO.model_validate(payload)


@pytest.fixture(scope="session")
def access_token(access_token_dto: DecodedTokenDTO) -> str:
    settings = get_settings(TestSettings)
    token_data = access_token_dto.model_dump()
    token_data["sub"] = str(token_data["sub"])
    return jwt.encode(
        payload=token_data,
        key=settings.auth_private_key,
        algorithm=get_settings(KeycloakSettings).encoding_algorithm,
    )


@pytest.fixture(scope="session")
async def keycloack_mock(test_container: TestContainer) -> AsyncIterator[Mock]:
    mock = MagicMock(KeycloakService[DecodedTokenDTO])
    with test_container.override(
        aioinject.Object(mock, KeycloakService[DecodedTokenDTO])
    ):
        yield mock


@pytest.fixture(scope="session", autouse=True)
async def _autouse_keycloack_mock(  # pyright: ignore[reportUnusedFunction]
    keycloack_mock: Mock,
    access_token_dto: DecodedTokenDTO,
) -> None:
    settings = get_settings(TestSettings)
    public_key = settings.auth_public_key.removeprefix(
        "-----BEGIN PUBLIC KEY-----\n",
    ).removesuffix(
        "\n-----END PUBLIC KEY-----",
    )
    keycloack_mock.get_public_key.return_value = public_key
    keycloack_mock.decode_token.return_value = Ok(access_token_dto)
