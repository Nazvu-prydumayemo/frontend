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
    def __init__(self, client: APIClient) -> None:
        self._client = client

    async def me(self) -> UserResult:
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
