from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        api_url: The base URL of the API backend.
        api_token: The authentication token for the API (optional).
    """

    service_name: str
    key_name: str
    api_url: AnyHttpUrl

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()  # type: ignore[call-arg]
