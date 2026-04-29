"""Authentication service for handling login, registration, and user information."""

from tuiapp.api.auth.schema import (
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    Token,
    TokenResult,
    VerifyResetCodeRequest,
)
from tuiapp.api.client import APIClient
from tuiapp.api.errors import APIError
from tuiapp.api.schema import Message, Result


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
            if error.status_code in (400, 401, 403, 422):
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

            elif error.status_code == 422:
                return TokenResult(token=None, message="Weak password", status="error")

            else:
                return TokenResult(
                    token=None, message=f"Server error: {error.status_code}", status="error"
                )

    async def forgot_password(self, json: ForgotPasswordRequest) -> Result:
        try:
            response = await self._client.post(
                "/auth/forgot-password", json=json, response_model=Message
            )
            return Result(message=response.message, status="success")

        except APIError as error:
            if error.status_code == 422:
                return Result(message=error.message, status="error")

            return Result(message=f"Server error: {error.status_code}", status="error")

    async def verify_reset_code(self, json: VerifyResetCodeRequest) -> Result:
        try:
            response = await self._client.post(
                "/auth/verify-reset-code", json=json, response_model=Message
            )
            return Result(message=response.message, status="success")

        except APIError as error:
            if error.status_code == 401:
                return Result(message="Invalid or expired Reset Code", status="invalid")

            if error.status_code == 404:
                return Result(message="The given user does not exist", status="error")

            if error.status_code == 422:
                return Result(message=error.message, status="error")

            return Result(message=f"Server error: {error.status_code}", status="error")
