import ssl

from faststream.security import SASLPlaintext
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kafka_")

    sasl_username: str | None = None
    sasl_password: str | None = None
    ssl_crt_path: str = ""

    bootstrap_servers: str = "localhost:9092"
    group_id: str = "backend"
    max_poll_records: int = 500

    def get_ssl_context(self) -> ssl.SSLContext | None:  # pragma: no cover
        if not self.ssl_crt_path:
            return None

        ctx = ssl.create_default_context(cafile=self.ssl_crt_path)
        ctx.check_hostname = False
        return ctx

    def get_security(self) -> SASLPlaintext | None:  # pragma: no cover
        if not (self.ssl_crt_path and self.sasl_username and self.sasl_password):
            return None
        return SASLPlaintext(
            username=self.sasl_username,
            password=self.sasl_password,
            ssl_context=self.get_ssl_context(),
            use_ssl=True,
        )
