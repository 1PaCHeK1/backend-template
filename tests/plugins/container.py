from collections.abc import AsyncIterator

import aioinject
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="session")
def container() -> aioinject.Container:
    from app.di import create_container

    return create_container()


@pytest.fixture
async def injection_context(
    container: aioinject.Container,
    session: AsyncSession,
) -> AsyncIterator[aioinject.InjectionContext]:
    with container.override(
        aioinject.Object(session, type_=AsyncSession),
    ):
        async with container.context() as ctx:
            yield ctx
