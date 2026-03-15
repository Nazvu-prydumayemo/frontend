from tuiapp.api.auth.schema import LoginRequest, RegisterRequest, Token, TokenResult
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError


class AuthService:
    def __init__(self, client: APIClient) -> None:
        self._client = client

    async def login(self, json: LoginRequest) -> TokenResult:
        try:
            token = await self._client.post("/auth/login", json=json, response_model=Token)
            return TokenResult(token=token, message="Login successful", status="success")

        except APIError as error:
            if error.status_code in (400, 401, 403):
                return TokenResult(
                    token=None, message="Invalid username or password", status="invalid"
                )

            else:
                return TokenResult(
                    token=None, message=f"Server error: {error.status_code}", status="error"
                )

    async def register(self, json: RegisterRequest) -> TokenResult:
        try:
            token = await self._client.post("/auth/register", json=json, response_model=Token)
            return TokenResult(token=token, message="Register successful", status="success")

        except APIError as error:
            if error.status_code == 400:
                return TokenResult(token=None, message="User already exists", status="error")

            else:
                return TokenResult(
                    token=None, message=f"Server error: {error.status_code}", status="error"
                )
