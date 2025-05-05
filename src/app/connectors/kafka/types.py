import ssl
from typing import Literal, NotRequired, TypedDict

from pydantic_settings import BaseSettings


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
