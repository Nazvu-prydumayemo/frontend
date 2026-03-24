"""Account service for managing user account operations."""

from tuiapp.api.account.schema import (
    Delete,
    DeleteRequest,
    PasswordRequest,
    ProfileRequest,
    User,
    UserResult,
)
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError
from tuiapp.api.schema import Result


class AccountService:
    """Service for managing user account operations.

    Provides methods for fetching user profile, updating personal information,
    changing password, and deleting the account.

    Attributes:
        _client: The API client used for making requests.
    """

    def __init__(self, client: APIClient) -> None:
        """Initialize the AccountService.

        Args:
            client: The APIClient instance for making API requests.
        """
        self._client = client

    async def me(self) -> UserResult:
        """Fetch the current user's profile information.

        Calls the /account/me endpoint to retrieve the authenticated user's
        details including firstname, lastname, email, and account status.

        Returns:
            UserResult: Contains the user data on success, or error status and message on failure.
        """
        try:
            response = await self._client.get("/account/me", User)
            return UserResult(user=response, message="Authenticated", status="success")

        except APIError as error:
            if error.status_code == 401:
                return UserResult(user=None, message="Not Authenticated", status="invalid")

            return UserResult(
                user=None, message=f"Server error: {error.status_code}", status="error"
            )

    async def profile(self, json: ProfileRequest) -> UserResult:
        """Update the user's profile information.

        Sends a PATCH request to /account/profile with the provided firstname
        and/or lastname to update the user's personal information.

        Args:
            json: ProfileRequest containing the fields to update.

        Returns:
            UserResult: Contains updated user data on success, or error status and message on failure.
        """
        try:
            response = await self._client.patch("/account/profile", json=json, response_model=User)
            return UserResult(
                user=response, message="Successfully changed personal information", status="success"
            )

        except APIError as error:
            if error.status_code == 401:
                return UserResult(user=None, message="Not Authenticated", status="invalid")

            return UserResult(
                user=None, message=f"Server error: {error.status_code}", status="error"
            )

    async def change_password(self, json: PasswordRequest) -> UserResult:
        """Change the user's password.

        Sends a POST request to /account/change-password with the current
        and new password to update the user's password.

        Args:
            json: PasswordRequest containing current and new password.

        Returns:
            UserResult: Contains success message on success, or error status and message on failure.
        """
        try:
            response = await self._client.post(
                "/account/change-password", json=json, response_model=User
            )
            return UserResult(
                user=response, message="Successfully changed password", status="success"
            )

        except APIError as error:
            if error.status_code == 400:
                return UserResult(
                    user=None,
                    message="New password cannot be the same as the old password",
                    status="invalid",
                )

            elif error.status_code == 401:
                return UserResult(
                    user=None,
                    message="Current password is incorrect",
                    status="invalid",
                )

            return UserResult(
                user=None, message=f"Server error: {error.status_code}", status="error"
            )

    async def delete(self, json: DeleteRequest) -> Result:
        """Delete the user's account.

        Sends a POST request to /account/delete with the user's password
        to permanently delete the account.

        Args:
            json: DeleteRequest containing the user's password for verification.

        Returns:
            Result: Contains success message on success, or error status and message on failure.
        """
        try:
            await self._client.post("account/delete", json=json, response_model=Delete)
            return Result(message="Account deleted successfully", status="success")

        except APIError as error:
            if error.status_code == 401:
                return Result(message="Not Authenticated", status="invalid")

            elif error.status_code == 403:
                return Result(
                    message="Password is incorrect",
                    status="invalid",
                )

            return Result(message=f"Server error: {error.status_code}", status="error")
