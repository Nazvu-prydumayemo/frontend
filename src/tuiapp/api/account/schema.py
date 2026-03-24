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
    message: str


class ProfileRequest(BaseModel):
    firstname: str | None
    lastname: str | None


class PasswordRequest(BaseModel):
    current_password: str
    new_password: str


class DeleteRequest(BaseModel):
    password: str


class UserResult(Result):
    user: User | None
