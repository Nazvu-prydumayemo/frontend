from datetime import date

from pydantic import BaseModel

from tuiapp.api.court.schema import CourtScheduleSlot
from tuiapp.api.schema import Result


class OrderRequest(BaseModel):
    court_id: int
    booking_slot_ids: list[int]


class OrderDetail(BaseModel):
    id: int
    user_id: int
    court_id: int
    booking_date: date
    total_price: float
    created_at: str


class OrderDetailResult(Result):
    orders: list[OrderDetail] | None


class Order(OrderDetail):
    booking_slots: list[CourtScheduleSlot]


class OrderResult(Result):
    order: Order | None
