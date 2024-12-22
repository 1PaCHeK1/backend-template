import pkgutil

import dotenv
import pytest
from _pytest.fixtures import SubRequest

import tests.entities
import tests.plugins

dotenv.load_dotenv(".env", override=True)

pytest_plugins = [
    "anyio",
    "sqlalchemy_pytest.database",
    *(
        mod.name
        for mod in pkgutil.walk_packages(
            tests.plugins.__path__,
            prefix="tests.plugins.",
        )
        if not mod.ispkg
    ),
    *(
        mod.name
        for mod in pkgutil.walk_packages(
            tests.entities.__path__,
            prefix="tests.entities.",
        )
        if not mod.ispkg
    ),
]


@pytest.fixture(scope="session", autouse=True)
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def worker_id() -> str:
    return "main"


@pytest.fixture(params=[0, 1, 7])
def collection_size(request: SubRequest) -> int:
    return request.param  # type: ignore[no-any-return]
