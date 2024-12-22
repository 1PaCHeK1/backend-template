from http import HTTPMethod
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="api_")

    cors_allow_origins: list[str] = []
    cors_allow_methods: list[Literal["*"] | HTTPMethod] = ["*"]
    cors_allow_headers: list[str] = ["authorization"]
