from __future__ import annotations

import functools
import importlib
import pkgutil
from collections.abc import Iterable, Mapping, Sequence
from types import ModuleType
from typing import TYPE_CHECKING, Any

import aioinject
from aioinject import Provider, Scope
from aioinject.extensions import ProviderExtension
from aioinject.extensions.providers import (
    CacheDirective,
    ProviderInfo,
    ResolveDirective,
)
from pydantic_settings import BaseSettings

from lib.settings import get_settings

if TYPE_CHECKING:
    from aioinject._internal.type_sources import TypeResolver


type Providers = Iterable[Provider[Any]]


def autodiscover_providers(
    module: ModuleType,
    attr_name: str,
    *,
    raise_error: bool = True,
) -> Sequence[Provider[object]]:
    result: list[Provider[object]] = []
    for submodule_info in pkgutil.walk_packages(module.__path__, f"{module.__name__}."):
        submodule = importlib.import_module(submodule_info.name)
        module_providers = getattr(submodule, attr_name, None)
        if module_providers is None:
            if raise_error:
                msg = (
                    f"Module {submodule_info.name} does not have {attr_name} attribute"
                )
                raise ValueError(msg)
            continue
        result.extend(module_providers)
    return result


def register_settings[T: BaseSettings](settings_cls: type[T]) -> aioinject.Singleton[T]:
    factory = functools.partial(get_settings, settings_cls)
    return aioinject.Singleton(factory, interface=settings_cls)


class SettingsProvider[T: BaseSettings](Provider[T]):
    def __init__(self, settings_cls: type[T]) -> None:
        self.implementation = settings_cls

    def provide(self, kwargs: dict[str, Any]) -> T:  # noqa: ARG002
        return self.implementation()


class SettingsProviderExtension[T: BaseSettings](
    ProviderExtension[SettingsProvider[T]],
):
    def supports_provider(self, provider: object) -> bool:
        return isinstance(provider, SettingsProvider)

    def extract(
        self,
        provider: SettingsProvider[T],
        type_context: Mapping[str, type[object]],  # noqa: ARG002
        type_resolver: TypeResolver,  # noqa: ARG002
    ) -> ProviderInfo[T]:
        return ProviderInfo(
            interface=provider.implementation,
            type_=provider.implementation,
            dependencies=(),
            scope=Scope.lifetime,
            compilation_directives=(
                ResolveDirective(is_async=False, is_context_manager=False),
                CacheDirective(),
            ),
        )
