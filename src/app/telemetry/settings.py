import enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingLevel(enum.StrEnum):
    DEBUG = enum.auto()
    INFO = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()
    CRITICAL = enum.auto()


class SentryEnvironment(enum.StrEnum):
    development = enum.auto()
    staging = enum.auto()
    production = enum.auto()


class SentrySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="sentry_")

    dsn: str = ""
    environment: SentryEnvironment = SentryEnvironment.production
    traces_sample_rate: float = Field(default=1.0, ge=0.0, le=1.0)


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="logging_")

    level: LoggingLevel = LoggingLevel.INFO
