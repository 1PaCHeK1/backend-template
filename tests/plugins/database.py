import pytest
from sqlalchemy.ext import asyncio

import app.storages.db.base.engine
from alembic import config
from lib.settings import get_settings
from tests.settings import TestSettings


@pytest.fixture(scope="session")
def database_url() -> str:
    return get_settings(TestSettings).database_url


@pytest.fixture(scope="session")
def async_sessionmaker() -> asyncio.async_sessionmaker[asyncio.AsyncSession]:
    return app.storages.db.base.engine.async_session_factory


@pytest.fixture(scope="session")
def alembic_config() -> config.Config | None:
    return config.Config("alembic.ini")
