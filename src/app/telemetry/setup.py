import logging

import sentry_sdk

from app.telemetry.settings import LoggingSettings, SentrySettings
from lib.settings import get_settings


def setup_telemetry(*, source: str | None = None) -> None:
    sentry_settings = get_settings(SentrySettings)
    sentry_sdk.init(
        dsn=sentry_settings.dsn,
        environment=sentry_settings.environment.name,
        traces_sample_rate=sentry_settings.traces_sample_rate,
    )
    sentry_sdk.set_tag("source", source or "unset")

    logging_settings = get_settings(LoggingSettings)
    logging.basicConfig(level=logging_settings.level.name)
