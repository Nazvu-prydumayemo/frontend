"""Pydantic schemas for account API requests and responses."""

from datetime import date, time

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


class ExportSlot(BaseModel):
    """A single slot within an exported order.

    Attributes:
        court_id: The ID of the court.
        slot_date: The date of the slot.
        start_time: The starting time of the slot.
        end_time: The ending time of the slot.
    """

    model_config = {"extra": "ignore"}
    court_id: int
    slot_date: date
    start_time: time
    end_time: time


class DataExportOrder(BaseModel):
    """An order within a data export.

    Attributes:
        order_id: The unique identifier of the order.
        court_id: The ID of the booked court.
        booking_date: The date of the booking.
        total_price: The total price of the order.
        created_at: The timestamp when the order was created.
        slots: The list of booked slots for this order.
    """

    model_config = {"extra": "ignore"}
    order_id: int
    court_id: int
    booking_date: date | None = None
    total_price: str | None = None
    created_at: str | None = None
    slots: list[ExportSlot] = []


class DataExport(BaseModel):
    """Response model for user data export.

    Attributes:
        profile: The user's profile information.
        orders: The list of orders associated with the user.
    """

    profile: User
    orders: list[DataExportOrder]


class DataExportResult(Result):
    """Result model for data export operations.

    Attributes:
        data_export: The exported user data on success, None on failure.
        message: A descriptive message about the result.
        status: The status of the operation (success, invalid, or error).
    """

    data_export: DataExport | None
