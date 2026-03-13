from tuiapp.api.auth.schema import LoginRequest, Token
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError


class AuthService:
    def __init__(self, client: APIClient) -> None:
        self._client = client

    async def login(self, json: LoginRequest) -> Token | None:
        try:
            return await self._client.post("/auth/login", json=json, response_model=Token)

        except APIError as error:
            if error.status_code == 400 or error.status_code == 401:
                return None

            raise
