import pydantic
from pydantic import AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="test_")

    use_casefold: bool = True

    database_url: str = pydantic.Field(
        validation_alias=AliasChoices(
            "DATABASE_TEST_URL",
            "TEST_DATABASE_URL",
        ),
    )
    auth_public_key: str
    auth_private_key: str
