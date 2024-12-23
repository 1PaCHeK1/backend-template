import contextlib
from collections.abc import AsyncIterator
from typing import TypeVar

import aioinject
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.storages.db.base.engine import async_engine, async_session_factory
from app.storages.db.uow import UnitOfWork
from lib.di import Providers

TBase = TypeVar("TBase", bound=DeclarativeBase)


@contextlib.asynccontextmanager
async def get_engine() -> AsyncIterator[AsyncEngine]:
    yield async_engine
    await async_engine.dispose()


@contextlib.asynccontextmanager
async def get_session(
    engine: AsyncEngine,  # noqa: ARG001
) -> AsyncIterator[AsyncSession]:
    async with async_session_factory.begin() as session:
        yield session


providers: Providers = [
    aioinject.Singleton(get_engine),
    aioinject.Scoped(get_session),
    aioinject.Scoped(UnitOfWork),
]
