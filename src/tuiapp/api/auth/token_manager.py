"""Token manager service for handling access and refresh tokens."""

import keyring
import keyring.errors

from tuiapp.api.auth.schema import RefreshRequest, Token
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError
from tuiapp.settings import settings


class TokenManagerService:
    """Manages access and refresh tokens with secure storage.

    Handles storage of refresh tokens in the system keyring and provides
    methods for token refresh and cleanup.

    Attributes:
        _client: The API client used for refresh requests.
        access_token: The current access token (in-memory only).
    """

    def __init__(self, client: APIClient) -> None:
        """Initialize the TokenManagerService.

        Args:
            client: The APIClient instance for making refresh requests.
        """
        self._client = client
        self.access_token: str | None = None

    def set_refresh_token(self, refresh_token: str) -> None:
        """Store the refresh token securely in the system keyring.

        Args:
            refresh_token: The refresh token to store.
        """
        keyring.set_password(settings.service_name, settings.key_name, refresh_token)

    def get_refresh_token(self) -> str | None:
        """Retrieve the refresh token from the system keyring.

        Returns:
            The stored refresh token, or None if not found.
        """
        return keyring.get_password(settings.service_name, settings.key_name)

    def clear_tokens(self) -> None:
        """Clear all stored tokens.

        Removes the access token from memory and deletes the refresh token
        from the system keyring.
        """
        self.access_token = None
        self._client.set_access_token(None)

        try:
            keyring.delete_password(settings.service_name, settings.key_name)
        except keyring.errors.PasswordDeleteError:
            pass

    async def refresh_access_token(self) -> bool:
        """Attempt to refresh the access token using the stored refresh token.

        Sends a refresh request to the backend API. On success, updates
        the in-memory access token and persists the new refresh token.

        Returns:
            True if token refresh was successful, False otherwise.
        """
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
