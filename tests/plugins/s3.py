from collections.abc import AsyncIterator

import aioinject
import pytest

from app.storages.s3.settings import S3Settings
from app.storages.s3.storage import S3Storage


@pytest.fixture
async def s3_mock(container: aioinject.Container) -> AsyncIterator[None]:
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
    with container.override(
        aioinject.Object(settings, type_=S3Settings),
        aioinject.Object(s3_storage, type_=S3Storage),
    ):
        yield
