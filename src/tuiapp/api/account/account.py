from tuiapp.api.account.schema import MeResponse
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError


class AccountService:
    def __init__(self, client: APIClient) -> None:
        self._client = client

    async def me(self) -> MeResponse | None:
        try:
            response = await self._client.get("/account/me", MeResponse)
            return response

        except APIError:
            return None
