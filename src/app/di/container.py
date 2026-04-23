import functools
from typing import TYPE_CHECKING

import aioinject
from aioinject.ext.fastapi import FastAPIExtension
from pydantic_settings import BaseSettings

from app.di import _modules
from lib.di import SettingsProviderExtension, autodiscover_providers


def create_container() -> aioinject.Container:
    container = aioinject.Container(
        extensions=[
            SettingsProviderExtension[BaseSettings](),
            FastAPIExtension(),
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
