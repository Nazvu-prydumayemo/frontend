from tuiapp.api.account.schema import MeResult, PasswordRequest, ProfileRequest, User
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError


class AccountService:
    def __init__(self, client: APIClient) -> None:
        self._client = client

    async def me(self) -> MeResult:
        try:
            response = await self._client.get("/account/me", User)
            return MeResult(user=response, message="Authenticated", status="success")

        except APIError as error:
            if error.status_code == 401:
                return MeResult(user=None, message="Not Authenticated", status="invalid")

            return MeResult(user=None, message=f"Server error: {error.status_code}", status="error")

    async def profile(self, json: ProfileRequest) -> MeResult:
        try:
            response = await self._client.patch("/account/profile", json=json, response_model=User)
            return MeResult(
                user=response, message="Successfully changed personal information", status="success"
            )

        except APIError as error:
            if error.status_code == 401:
                return MeResult(user=None, message="Not Authenticated", status="invalid")

            return MeResult(user=None, message=f"Server error: {error.status_code}", status="error")

    async def change_password(self, json: PasswordRequest) -> MeResult:
        try:
            response = await self._client.post(
                "/account/change-password", json=json, response_model=User
            )
            return MeResult(
                user=response, message="Successfully changed password", status="success"
            )

        except APIError as error:
            if error.status_code == 400:
                return MeResult(
                    user=None,
                    message="New password cannot be the same as the old password",
                    status="invalid",
                )

            elif error.status_code == 401:
                return MeResult(
                    user=None,
                    message="Current password is incorrect",
                    status="invalid",
                )

            return MeResult(user=None, message=f"Server error: {error.status_code}", status="error")
