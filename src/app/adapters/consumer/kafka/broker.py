from faststream.kafka import KafkaBroker

from app.adapters.consumer.kafka.router import router
from app.adapters.consumer.kafka.settings import KafkaSettings
from app.adapters.consumer.middlewares import AioinjectMiddleware


def create_broker(settings: KafkaSettings) -> KafkaBroker:
    broker = KafkaBroker(
        bootstrap_servers=settings.bootstrap_servers,
        client_id=settings.group_id,
        max_batch_size=settings.max_poll_records,
        security=settings.get_security(),
        middlewares=[
            AioinjectMiddleware,
        ],
    )
    broker.include_router(router)
    return broker
