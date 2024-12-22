import functools
from collections.abc import Iterable
from typing import TYPE_CHECKING

import aioinject
from pydantic_settings import BaseSettings

from app.connectors.keycloak.settings import KeycloakSettings
from app.core.di import _modules
from app.storages.db.settings import DatabaseSettings
from app.storages.s3.settings import S3Settings
from lib.di import autodiscover_providers
from lib.settings import get_settings


def _register_settings(
    container: aioinject.Container,
    settings_classes: Iterable[type[BaseSettings]],
) -> None:
    for settings_cls in settings_classes:
        factory = functools.partial(get_settings, settings_cls)
        container.register(aioinject.Singleton(factory, type_=settings_cls))


def create_container() -> aioinject.Container:
    container = aioinject.Container()

    _register_settings(
        container=container,
        settings_classes=[
            DatabaseSettings,
            S3Settings,
            KeycloakSettings,
        ],
    )
    for provider in autodiscover_providers(
        _modules,
        attr_name="providers",
        raise_error=False,
    ):
        container.register(provider)

    return container


if not TYPE_CHECKING:  # pragma: no cover
    create_container = functools.lru_cache(create_container)
