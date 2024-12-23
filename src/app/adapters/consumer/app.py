import contextlib
from collections.abc import AsyncIterator
from typing import Any

from faststream import FastStream
from faststream.asgi import AsgiFastStream, make_ping_asgi
from faststream.broker.core.usecase import BrokerUsecase

from app.adapters.consumer.kafka.broker import create_broker
from app.adapters.consumer.kafka.settings import KafkaSettings
from app.di.container import create_container
from app.version import __version__
from lib.settings import get_settings


@contextlib.asynccontextmanager
async def _lifespan() -> AsyncIterator[None]:
    async with create_container():
        yield


def create_app(broker: BrokerUsecase[Any, Any]) -> FastStream:
    return FastStream(
        broker=broker,
        lifespan=_lifespan,
        title="Title",
        description="Description",
        version=__version__,
    )


def create_kafka_app() -> AsgiFastStream:
    kafka_settings = get_settings(KafkaSettings)
    broker = create_broker(kafka_settings)

    return create_app(broker).as_asgi(
        asgi_routes=(("kafka/health", make_ping_asgi(broker, timeout=5.0)),),
        asyncapi_path="/kafka/docs",
    )
