import functools
from collections.abc import Callable
from typing import Any, TypeVar
from uuid import UUID

from polyfactory import BaseFactory
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from pydantic import BaseModel
from uuid_utils.compat import uuid7

T = TypeVar("T")
TBaseModel = TypeVar("TBaseModel", bound=BaseModel)


def random_string(
    max_chars: int = 64,
    min_chars: int = 1,
) -> Callable[[], str]:
    return functools.partial(BaseFactory.__faker__.pystr, min_chars, max_chars)


PROVIDER_MAP = {
    UUID: uuid7,
}


class SQLAlchemyBaseFactory(SQLAlchemyFactory[T]):
    __is_base_factory__ = True
    __use_defaults__ = True
    __set_foreign_keys__ = False

    @classmethod
    def get_provider_map(cls) -> dict[Any, Callable[[], Any]]:
        base_provider_map = super().get_provider_map()
        return {
            **base_provider_map,
            **PROVIDER_MAP,  # type: ignore[dict-item]
        }


class PydanticBaseFactory(ModelFactory[TBaseModel]):
    __is_base_factory__ = True

    @classmethod
    def get_provider_map(cls) -> dict[Any, Callable[[], Any]]:
        base_provider_map = super().get_provider_map()
        return {
            **base_provider_map,
            **PROVIDER_MAP,  # type: ignore[dict-item]
        }
