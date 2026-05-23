"""Pydantic schemas for order API requests and responses."""

from datetime import date

from pydantic import BaseModel

from tuiapp.api.court.schema import CourtScheduleSlot
from tuiapp.api.schema import Result


class OrderRequest(BaseModel):
    """Request model for creating a new booking order.

    Attributes:
        court_id: The ID of the court to book.
        booking_slot_ids: The list of slot IDs to book.
    """

    court_id: int
    booking_slot_ids: list[int]


class OrderDetail(BaseModel):
    """Response model for order summary information.

    Attributes:
        id: The unique identifier of the order.
        user_id: The ID of the user who placed the order.
        court_id: The ID of the booked court.
        booking_date: The date of the booking.
        total_price: The total price of the order.
        created_at: The timestamp when the order was created.
    """

    id: int
    user_id: int
    court_id: int
    booking_date: date
    total_price: float
    created_at: str


class OrderDetailResult(Result):
    """Result model for listing orders operations.

    Attributes:
        orders: The list of orders on success, None on failure.
        message: A descriptive message about the result.
        status: The status of the operation (success, invalid, or error).
    """

    orders: list[OrderDetail] | None


class Order(OrderDetail):
    """Response model for a full order including booked slots.

    Attributes:
        booking_slots: The list of booked slots for this order.
    """

    booking_slots: list[CourtScheduleSlot]


class OrderResult(Result):
    """Result model for individual order operations.

    Attributes:
        order: The order data on success, None on failure.
        message: A descriptive message about the result.
        status: The status of the operation (success, invalid, or error).
    """

    order: Order | None
