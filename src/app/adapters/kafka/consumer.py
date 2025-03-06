from collections.abc import Sequence
from typing import Any

import orjson
from aiokafka import AIOKafkaConsumer, ConsumerRecord, TopicPartition
from result import Err

from app.connectors.kafka.types import KafkaConsumerSettings, TopicConfig
from app.di.container import create_container


async def create_consumer(
    *,
    topics: Sequence[str],
    settings: KafkaConsumerSettings,
    group_instance_id: str | None = None,
) -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        *topics,
        bootstrap_servers=settings.bootsrap_servers,
        group_id=settings.group_id,
        group_instance_id=group_instance_id,
        enable_auto_commit=False,
        value_deserializer=orjson.loads,
        auto_offset_reset="earliest",
        **settings.get_security(),
    )


async def consume(
    *,
    consumer: AIOKafkaConsumer,
    topic_configs: Sequence[TopicConfig[Any, Any]],
) -> None:
    config_map = {config.topic: config for config in topic_configs}

    async with consumer, create_container() as container:
        async for message in consumer:
            message: ConsumerRecord[Any, bytes]
            async with container.context() as ctx:
                config = config_map[message.topic]
                mapper = await ctx.resolve(config.mapper)

                decoded_message = await mapper.process(message.value)
                if isinstance(decoded_message, Err):
                    raise decoded_message.err_value

                worker = await ctx.resolve(config.worker)

                result = await worker.process(decoded_message.ok_value)
                if isinstance(result, Err):
                    raise result.err_value

                tp = TopicPartition(message.topic, message.partition)
                await consumer.commit({tp: message.offset + 1})
