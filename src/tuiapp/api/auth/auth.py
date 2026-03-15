from tuiapp.api.auth.schema import LoginRequest, LoginResult, Token
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError


class AuthService:
    def __init__(self, client: APIClient) -> None:
        self._client = client

    async def login(self, json: LoginRequest) -> LoginResult:
        try:
            token = await self._client.post("/auth/login", json=json, response_model=Token)
            return LoginResult(token=token, message="Login successful", status="success")

        except APIError as error:
            if error.status_code in (400, 401, 403):
                return LoginResult(
                    token=None, message="Invalid username or password", status="invalid"
                )

            else:
                return LoginResult(
                    token=None, message=f"Server error: {error.status_code}", status="error"
                )
