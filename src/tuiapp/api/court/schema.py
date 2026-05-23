"""Pydantic schemas for court API requests and responses."""

from datetime import date, time
from enum import Enum

from pydantic import BaseModel

from tuiapp.api.schema import Result


class Day(Enum):
    """Enum representing days of the week."""

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Court(BaseModel):
    """Response model for court information.

    Attributes:
        id: The unique identifier of the court.
        created_at: The timestamp when the court was created.
        name: The name of the court.
        description: A description of the court.
        surface_type: The type of surface (e.g., clay, hard, grass).
        is_indoor: Whether the court is indoors.
        location: The location of the court.
        price_per_hour: The price per hour for booking.
        working_hours: The working hours of the court.
    """

    id: int
    created_at: str

    name: str
    description: str | None = None

    surface_type: str
    is_indoor: bool

    location: str | None = None
    price_per_hour: float
    working_hours: str | None = None


class CourtSchedule(BaseModel):
    """Response model for court schedule information.

    Attributes:
        day_of_week: The day of the week for this schedule entry.
        opening_time: The opening time for the court on this day.
        closing_time: The closing time for the court on this day.
        id: The unique identifier of the schedule entry.
        court_id: The ID of the court.
        created_at: The timestamp when the schedule was created.
    """

    day_of_week: Day
    opening_time: time | None
    closing_time: time | None
    id: int
    court_id: int
    created_at: str


class CourtScheduleSlot(BaseModel):
    """Response model for a single court schedule slot.

    Attributes:
        start_time: The start time of the slot.
        end_time: The end time of the slot.
        id: The unique identifier of the slot.
        court_id: The ID of the court.
        slot_date: The date of the slot.
        is_available: Whether the slot is available for booking.
        order_id: The ID of the order if the slot is booked.
        created_at: The timestamp when the slot was created.
    """

    start_time: time
    end_time: time
    id: int
    court_id: int
    slot_date: date
    is_available: bool
    order_id: int | None = None
    created_at: str


class CourtScheduleSlotsAll(BaseModel):
    """Response model for all available slots on a given date.

    Attributes:
        court_id: The ID of the court.
        slot_date: The date of the slots.
        available_slots: The list of available slots.
        total_slots: The total number of slots for the day.
    """

    court_id: int
    slot_date: date
    available_slots: list[CourtScheduleSlot]
    total_slots: int


class CourtScheduleSlotsAllResult(Result):
    """Result model for court available slots operations.

    Attributes:
        slots: The available slots data on success, None on failure.
        message: A descriptive message about the result.
        status: The status of the operation (success, invalid, or error).
    """

    slots: CourtScheduleSlotsAll | None


class CourtScheduleResult(Result):
    """Result model for court schedule operations.

    Attributes:
        schedule: The court schedule on success, None on failure.
        message: A descriptive message about the result.
        status: The status of the operation (success, invalid, or error).
    """

    schedule: list[CourtSchedule] | None


class CourtResult(Result):
    """Result model for individual court operations.

    Attributes:
        court: The court data on success, None on failure.
        message: A descriptive message about the result.
        status: The status of the operation (success, invalid, or error).
    """

    court: Court | None


class CourtsAll(BaseModel):
    """Response model for a paginated list of courts.

    Attributes:
        items: The list of courts.
        total: The total number of courts.
        skip: The number of courts skipped.
        limit: The maximum number of courts returned.
    """

    items: list[Court]
    total: int
    skip: int
    limit: int


class CourtsAllResult(Result):
    """Result model for listing all courts operations.

    Attributes:
        courts: The paginated courts data on success, None on failure.
        message: A descriptive message about the result.
        status: The status of the operation (success, invalid, or error).
    """

    courts: CourtsAll | None
