import keyring
import keyring.errors

from tuiapp.api.auth.schema import RefreshRequest, Token
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError
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

    async def refresh_access_token(self) -> bool:
        refresh_token = self.get_refresh_token()
        if not refresh_token:
            return False

        try:
            token = await self._client.post(
                "/auth/refresh",
                json=RefreshRequest(refresh_token=refresh_token),
                response_model=Token,
            )

            self.access_token = token.access_token
            self._client.set_access_token(token.access_token)
            self.set_refresh_token(token.refresh_token)

            return True

        except APIError as error:
            if error.status_code == 401:
                self.clear_tokens()

            return False
