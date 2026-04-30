from pydantic import BaseModel

from tuiapp.api.schema import Result


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


class CourtResult(Result):
    court: Court | None
