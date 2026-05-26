"""Token manager service for handling access and refresh tokens."""

import os
from typing import TYPE_CHECKING

import keyring
import keyring.errors

from tuiapp.api.auth.schema import RefreshRequest, Token
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError
from tuiapp.settings import settings

if TYPE_CHECKING:
    from tuiapp.app import TUIApplication


class TokenManagerService:
    """Manages access and refresh tokens with secure storage.

    Handles storage of refresh tokens in the system keyring and provides
    methods for token refresh and cleanup.

    Attributes:
        _client: The API client used for refresh requests.
        access_token: The current access token (in-memory only).
    """

    def __init__(self, client: APIClient, app: "TUIApplication | None" = None) -> None:
        """Initialize the TokenManagerService.

        Args:
            client: The APIClient instance for making refresh requests.
            app: Optional TUIApplication instance for redirects on auth failure.
        """
        self._client = client
        self._app = app
        self.access_token: str | None = None
        self._redirecting = False
        self._refresh_token: str | None = None
        self._use_keyring = os.environ.get("TEXTUAL_DRIVER") != "textual.drivers.web_driver:WebDriver"

    def set_refresh_token(self, refresh_token: str) -> None:
        """Store the refresh token.

        Uses in-memory storage in web mode (textual-serve) or system keyring otherwise.

        Args:
            refresh_token: The refresh token to store.
        """
        if self._use_keyring:
            keyring.set_password(settings.service_name, settings.key_name, refresh_token)
        else:
            self._refresh_token = refresh_token

    def get_refresh_token(self) -> str | None:
        """Retrieve the refresh token.

        Returns:
            The stored refresh token, or None if not found.
        """
        if self._use_keyring:
            return keyring.get_password(settings.service_name, settings.key_name)
        return self._refresh_token

    def clear_tokens(self) -> None:
        """Clear all stored tokens.

        Removes the access token from memory and deletes the refresh token
        from storage.
        """
        self.access_token = None
        self._client.set_access_token(None)
        self._refresh_token = None

        if self._use_keyring:
            try:
                keyring.delete_password(settings.service_name, settings.key_name)
            except keyring.errors.PasswordDeleteError:
                pass

    async def refresh_access_token(self) -> bool:
        """Attempt to refresh the access token using the stored refresh token.

        Sends a refresh request to the backend API. On success, updates
        the in-memory access token and persists the new refresh token.
        On failure, redirects to login screen.

        Returns:
            True if token refresh was successful, False otherwise.
        """
        refresh_token = self.get_refresh_token()
        if not refresh_token:
            self._redirect_to_main()
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
            self._redirecting = False
            return True

        except APIError as error:
            if error.status_code == 401:
                self.clear_tokens()

            self._redirect_to_login()
            return False

    def logout(self) -> None:
        """Log the user out and redirect to the main screen.

        Clears stored tokens and redirects the user to the main screen.
        """
        self.clear_tokens()
        self._redirect_to_main()

    def _redirect_to_main(self) -> None:
        """Redirect user to main if no token."""
        if self._app is None or self._redirecting:
            return
        self._redirecting = True

        def do_redirect():
            self._redirecting = False
            self._app.pop_screen()  # type: ignore
            self._app.push_screen("main")  # type: ignore

        self._app.call_later(do_redirect)

    def _redirect_to_login(self) -> None:
        """Redirect user to login screen when token refresh fails."""
        if self._app is None or self._redirecting:
            return
        self._redirecting = True

        def do_redirect():
            self._redirecting = False
            self._app.pop_screen()  # type: ignore
            self._app.push_screen("login")  # type: ignore

        self._app.call_later(do_redirect)
