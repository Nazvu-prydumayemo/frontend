"""Pydantic schemas for authentication API requests and responses."""

from pydantic import BaseModel, EmailStr

from tuiapp.api.schema import Result


class Token(BaseModel):
    """Response model containing access and refresh tokens.

    Attributes:
        access_token: The JWT access token for API requests.
        refresh_token: The token used to obtain new access tokens.
        token_type: The type of token (default: bearer).
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """Request model for user login.

    Attributes:
        email: The user's email address.
        password: The user's password.
    """

    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Request model for user registration.

    Attributes:
        firstname: The user's first name.
        lastname: The user's last name.
        email: The user's email address.
        password: The user's chosen password.
    """

    firstname: str
    lastname: str
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Request model for token refresh.

    Attributes:
        refresh_token: The refresh token to use for obtaining new access token.
    """

    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyResetCodeRequest(BaseModel):
    email: EmailStr
    code: str


class NewPassword(BaseModel):
    new_password: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str
    new_password: str


class TokenResult(Result):
    """Result model for authentication operations.

    Attributes:
        token: The Token object on success, None on failure.
        message: A descriptive message about the result.
        status: The status of the operation (success, invalid, or error).
    """

    token: Token | None
