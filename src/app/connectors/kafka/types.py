import ssl
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Any, ClassVar, Literal, NotRequired, TypedDict

from pydantic import Field
from pydantic_settings import BaseSettings

from lib.abc.mapper import MapperProtocol
from lib.abc.worker import WorkerProtocol


class SASLPlaintext(TypedDict):
    sasl_plain_username: NotRequired[str | None]
    sasl_plain_password: NotRequired[str | None]
    ssl_context: NotRequired[ssl.SSLContext | None]
    security_protocol: NotRequired[Literal["SASL_SSL"]]


class KafkaSettings(BaseSettings):
    bootsrap_servers: str = "127.0.0.1:9094"

    sasl_username: str | None = None
    sasl_password: str | None = None
    sasl_crt_path: str = ""

    def get_security(self) -> SASLPlaintext:
        if not self.sasl_crt_path:
            return SASLPlaintext()
        return SASLPlaintext(
            sasl_plain_username=self.sasl_username,
            sasl_plain_password=self.sasl_password,
            ssl_context=self.get_ssl_context(),
            security_protocol="SASL_SSL",
        )

    def get_ssl_context(self) -> ssl.SSLContext | None:
        if not self.sasl_crt_path:
            return None
        ctx = ssl.create_default_context(cafile=self.sasl_crt_path)
        ctx.check_hostname = False
        return ctx


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
