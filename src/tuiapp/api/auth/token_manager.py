import keyring
import keyring.errors

from tuiapp.api.client import APIClient
from tuiapp.settings import settings


class TokenManagerService:
    def __init__(self, client: APIClient) -> None:
        self._client = client
        self.access_token: str | None = None

    def set_refresh_token(self, refresh_token: str) -> None:
        keyring.set_password(settings.service_name, settings.key_name, refresh_token)

    def get_refresh_token(self) -> str | None:
        return keyring.get_password(settings.service_name, settings.key_name)

    def clear_tokens(self) -> None:
        self.access_token = None
        self._client.set_access_token(None)

        try:
            keyring.delete_password(settings.service_name, settings.key_name)
        except keyring.errors.PasswordDeleteError:
            pass
