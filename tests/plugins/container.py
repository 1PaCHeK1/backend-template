from collections.abc import AsyncIterator

import aioinject
import pytest
from aioinject.testing import TestContainer
from sqlalchemy.ext.asyncio import AsyncSession

from app.di import create_container


@pytest.fixture(scope="session")
def container() -> aioinject.Container:

    return create_container()


@pytest.fixture(scope="session")
def test_container(container: aioinject.Container) -> TestContainer:
    return TestContainer(container)


@pytest.fixture
async def injection_context(
    test_container: TestContainer,
    container: aioinject.Container,
    session: AsyncSession,
) -> AsyncIterator[aioinject.Context]:
    with test_container.override(
        aioinject.Object(session, interface=AsyncSession),
    ):
        async with container.context() as ctx:
            yield ctx
