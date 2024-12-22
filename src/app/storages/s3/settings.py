from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="s3_",
        case_sensitive=False,
        str_strip_whitespace=True,
    )

    endpoint_url: str
    bucket: str
    access_key: str
    secret_access_key: str
    addressing_style: Literal["path", "virtual"] = "virtual"
