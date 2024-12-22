from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

import aioinject
from aioboto3 import Session
from aiobotocore.config import AioConfig

from app.storages.s3 import S3Storage
from app.storages.s3.types import S3Client

if TYPE_CHECKING:
    from app.storages.s3.settings import S3Settings
    from lib.di import Providers


@contextlib.asynccontextmanager
async def get_s3_client(settings: S3Settings) -> AsyncIterator[S3Client]:
    session = Session(
        aws_access_key_id=settings.access_key,
        aws_secret_access_key=settings.secret_access_key,
    )
    client: S3Client
    async with session.client(  # pyright: ignore[reportGeneralTypeIssues]
        service_name="s3",
        endpoint_url=settings.endpoint_url,
        config=AioConfig(
            s3={"addressing_style": settings.addressing_style},
        ),
    ) as client:  # pyright: ignore[reportUnknownVariableType]
        yield client


def get_s3_storage(client: S3Client, settings: S3Settings) -> S3Storage:
    return S3Storage(
        client=client,
        bucket=settings.bucket,
        endpoint_url=settings.endpoint_url,
        addressing_style=settings.addressing_style,
    )


providers: Providers = [
    aioinject.Singleton(get_s3_client, type_=S3Client),
    aioinject.Scoped(get_s3_storage),
]
