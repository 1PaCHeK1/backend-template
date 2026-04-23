from collections.abc import AsyncIterator

import aioinject
import pytest
from aioinject.testing import TestContainer

from app.storages.s3.settings import S3Settings
from app.storages.s3.storage import S3Storage


@pytest.fixture
async def s3_mock(test_container: TestContainer) -> AsyncIterator[None]:
    settings = S3Settings(
        endpoint_url="https://test",
        bucket="test",
        access_key="test",
        secret_access_key="test",  # noqa: S106
    )
    s3_storage = S3Storage(
        client=None,  # type: ignore[arg-type]
        bucket=settings.bucket,
        endpoint_url=settings.endpoint_url,
    )
    with (
        test_container.override(aioinject.Object(settings, interface=S3Settings)),
        test_container.override(aioinject.Object(s3_storage, interface=S3Storage)),
    ):
        yield
