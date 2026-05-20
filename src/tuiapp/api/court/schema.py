from datetime import time
from enum import Enum

from pydantic import BaseModel

from tuiapp.api.schema import Result


class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Court(BaseModel):
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
    day_of_week: Day
    opening_time: time
    closing_time: time
    id: int
    court_id: int
    created_at: str


class CourtScheduleResult(Result):
    schedule: list[CourtSchedule] | None


class CourtResult(Result):
    court: Court | None


class CourtsAll(BaseModel):
    items: list[Court]
    total: int
    skip: int
    limit: int


class CourtsAllResult(Result):
    courts: CourtsAll | None
