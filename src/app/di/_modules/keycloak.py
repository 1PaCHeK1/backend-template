from __future__ import annotations

from typing import TYPE_CHECKING

import aioinject

from app.connectors.keycloak.command import Authenticator
from app.connectors.keycloak.dto import DecodedTokenDTO
from app.connectors.keycloak.service import KeycloakService
from app.connectors.keycloak.settings import KeycloakSettings
from lib.di import register_settings

if TYPE_CHECKING:
    from lib.di import Providers


def get_keycloak_service(
    settings: KeycloakSettings,
) -> KeycloakService[DecodedTokenDTO]:
    return KeycloakService[DecodedTokenDTO](
        token_dto=DecodedTokenDTO,
        server_url=settings.server_url,
        client_id=settings.client_id,
        realm_name=settings.realm_name,
        client_secret_key=settings.client_secret_key,
        encoding_algorithm=settings.encoding_algorithm,
    )


providers: Providers = [
    register_settings(KeycloakSettings),
    aioinject.Singleton(get_keycloak_service, type_=KeycloakService[DecodedTokenDTO]),
    aioinject.Scoped(Authenticator),
]
