import contextlib
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.storages.db.settings import DatabaseSettings


@contextlib.asynccontextmanager
async def create_engine(settings: DatabaseSettings) -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(
        settings.url,
        future=True,
        pool_size=20,
        pool_pre_ping=True,
        pool_use_lifo=True,
        echo=settings.echo,
    )
    yield engine
    await engine.dispose()


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine)


@contextlib.asynccontextmanager
async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    async with session_factory.begin() as session:
        yield session
