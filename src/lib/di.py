from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Iterable, Sequence
from types import ModuleType
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aioinject import Provider


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
