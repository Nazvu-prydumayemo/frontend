"""Pydantic schemas for account API requests and responses."""

from pydantic import BaseModel, EmailStr

from tuiapp.api.schema import Result


class User(BaseModel):
    """Response model for current user information.

    Attributes:
        firstname: The user's first name.
        lastname: The user's last name.
        email: The user's email address.
        id: The unique identifier of the user.
        role_id: The user's role identifier.
        is_active: Whether the user account is active.
    """

    firstname: str
    lastname: str
    email: EmailStr
    id: int
    role_id: int
    is_active: bool


class Delete(BaseModel):
    """Response model for account deletion confirmation.

    Attributes:
        message: Confirmation message from the server.
    """

    message: str


class ProfileRequest(BaseModel):
    """Request model for updating user profile information.

    Attributes:
        firstname: The user's first name (optional, null to leave unchanged).
        lastname: The user's last name (optional, null to leave unchanged).
    """

    firstname: str | None
    lastname: str | None


class PasswordRequest(BaseModel):
    """Request model for changing user password.

    Attributes:
        current_password: The user's current password for verification.
        new_password: The new password to set.
    """

    current_password: str
    new_password: str


class DeleteRequest(BaseModel):
    """Request model for deleting user account.

    Attributes:
        password: The user's current password for verification.
    """

    password: str


class UserResult(Result):
    """Result model for user-related operations.

    Extends Result to include user data on successful operations.

    Attributes:
        message: A descriptive message about the result.
        status: The status of the operation (success, invalid, or error).
        user: The User object on success, None on failure.
    """

    user: User | None
