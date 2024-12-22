from faststream.kafka import KafkaRouter

from app.adapters.consumer.kafka.schemas import TestSchema

router = KafkaRouter()


@router.subscriber("in-topic")
async def subscribe_handler(schema: TestSchema) -> None: ...
