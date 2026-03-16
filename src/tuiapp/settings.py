"""Application settings loaded from environment variables."""

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        service_name: The service name used for keyring storage.
        key_name: The key name used for storing refresh token in keyring.
        api_url: The base URL of the API backend.
    """

    service_name: str
    key_name: str
    api_url: AnyHttpUrl

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()  # type: ignore[call-arg]
