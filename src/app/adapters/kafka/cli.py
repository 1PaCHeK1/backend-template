import asyncio
import enum
from collections.abc import Mapping

import click
from aiokafka import TopicPartition

from app.adapters.kafka.consumer import consume, create_consumer
from app.adapters.kafka.types import KafkaConsumerSettings
from lib.asyncio import new_event_loop
from lib.settings import get_settings


class ClusterEnum(enum.StrEnum):
    example = enum.auto()


cluster_settings_map: Mapping[ClusterEnum, type[KafkaConsumerSettings]] = {}


@click.group()
def cli() -> None: ...


@cli.command("consume")
@click.argument("cluster", type=click.Choice(tuple(ClusterEnum)))
@click.option("--include", type=click.STRING, help="example: topic-a,topic-b,topic-c")
@click.option("--exclude", type=click.STRING, help="example: topic-a,topic-b,topic-c")
@click.option("--group-instance-id", type=click.STRING)
def cli_consume(
    cluster: str,
    include: str | None,
    exclude: str | None,
    group_instance_id: str | None,
) -> None:
    config_enum = ClusterEnum[cluster]
    if include and exclude:
        msg = "Include and exclude arguments that aren't provided together"
        raise click.BadArgumentUsage(msg)

    settings = get_settings(cluster_settings_map[config_enum])

    topic_configs = list(settings.topic_configs)
    if include is not None:
        topic_configs = [conf for conf in topic_configs if conf.topic in include]
    if exclude is not None:
        topic_configs = [conf for conf in topic_configs if conf.topic not in exclude]

    async def inner() -> None:
        consumer = await create_consumer(
            topics=[config.topic for config in topic_configs],
            settings=settings,
            group_instance_id=group_instance_id,
        )
        await consume(consumer=consumer, topic_configs=topic_configs)

    with asyncio.Runner(loop_factory=new_event_loop) as runner:
        runner.run(inner())


@cli.command("consume-partition")
@click.argument("cluster", type=click.Choice(tuple(ClusterEnum)))
@click.argument("topic", type=click.STRING)
@click.argument("partition", type=click.IntRange(min=0, max=10))
@click.option("--group-instance-id", type=click.STRING)
def cli_consume_partition(
    cluster: str,
    topic: str,
    partition: int,
    group_instance_id: str | None = None,
) -> None:
    config_enum = ClusterEnum[cluster]
    settings = get_settings(cluster_settings_map[config_enum])

    topic_config = next(
        (config for config in settings.topic_configs if config.topic == topic), None
    )
    if topic_config is None:
        msg = "Unknown topic"
        raise click.BadArgumentUsage(msg)

    async def inner() -> None:
        consumer = await create_consumer(
            topics=[],
            settings=settings,
            group_instance_id=group_instance_id,
        )
        consumer.assign([TopicPartition(topic=topic, partition=partition)])
        await consume(consumer=consumer, topic_configs=[topic_config])

    with asyncio.Runner(loop_factory=new_event_loop) as runner:
        runner.run(inner())


if __name__ == "__main__":
    cli()
