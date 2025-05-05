from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Any, ClassVar

from pydantic import Field

from app.connectors.kafka.types import KafkaSettings
from lib.abc.mapper import MapperProtocol
from lib.abc.worker import WorkerProtocol


@dataclass(kw_only=True, slots=True, frozen=True)
class TopicConfig[TInput, TResult]:
    topic: str
    mapper: type[MapperProtocol[TInput, TResult, Exception]]
    worker: type[WorkerProtocol[TResult, Any, Exception]]


class KafkaConsumerSettings(KafkaSettings):
    group_id: str = "backend"

    max_poll_records: int = 500
    topic_configs: Annotated[
        ClassVar[Sequence[TopicConfig[Any, Any]]],
        Field(init=False),
    ] = ()
