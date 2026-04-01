"""Application settings loaded from environment variables."""

import sys
from pathlib import Path

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


def get_env_file_path() -> Path:
    """Get the path to the .env file, handling PyInstaller bundling."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / ".env"  # type: ignore[attr-defined]
    else:
        return Path(__file__).parent.parent.parent / ".env"


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

    model_config = {"env_file": get_env_file_path(), "env_file_encoding": "utf-8"}


settings = Settings()  # type: ignore[call-arg]
