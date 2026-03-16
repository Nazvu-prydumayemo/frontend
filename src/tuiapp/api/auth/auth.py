"""Authentication service for handling login, registration, and user information."""

from tuiapp.api.auth.schema import LoginRequest, Me, RegisterRequest, Token, TokenResult
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError


class AuthService:
    """Service for handling authentication operations.

    Provides methods for user login, registration, and retrieving current user
    information via the backend API.

    Attributes:
        _client: The API client used for making HTTP requests.
    """

    def __init__(self, client: APIClient) -> None:
        """Initialize the AuthService with an API client.

        Args:
            client: The APIClient instance for making authenticated requests.
        """
        self._client = client

    async def login(self, json: LoginRequest) -> TokenResult:
        """Authenticate a user with email and password.

        Args:
            json: The login credentials containing email and password.

        Returns:
            TokenResult containing the access/refresh tokens on success,
            or an error message with status indicator on failure.
        """
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
        """Register a new user account.

        Args:
            json: The registration data containing user details.

        Returns:
            TokenResult containing the access/refresh tokens on success,
            or an error message with status indicator on failure.
        """
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

    async def me(self) -> str:
        """Retrieve the current authenticated user's information.

        Returns:
            A greeting message with user ID on success, or an error
            message on failure.
        """
        try:
            response = await self._client.get("/auth/me", response_model=Me)
            return f"Good Me! {response.id}"

        except APIError as error:
            if error.status_code in (400, 401, 403):
                return "Bad Me!"

            else:
                return "Bad Server Me!"
