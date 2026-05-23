"""Order card widget for displaying order summary information."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Click
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.api.order.schema import OrderDetail

MAX_LENGTH = 20


def truncate(value: str, max_length: int = MAX_LENGTH) -> str:
    """Truncate a string with ellipsis if it exceeds max_length."""
    if len(value) <= max_length:
        return value
    return value[:max_length].rstrip() + "..."


class OrderCard(Widget):
    """A card widget displaying summary information about an order."""

    DEFAULT_CLASSES = "order-card"

    selected: reactive[bool] = reactive(False)

    def watch_selected(self, value: bool) -> None:
        self.set_class(value, "selected")

    class Pressed(Message):
        """Posted when the order card is clicked."""

        def __init__(self, order_card: "OrderCard") -> None:
            super().__init__()
            self.order_card = order_card

    def __init__(
        self,
        order: OrderDetail,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.order = order

    def compose(self) -> ComposeResult:
        with Vertical(classes="order-card-body"):
            yield Static(
                f"Order #{self.order.id}",
                classes="order-card-id",
            )
            yield Static(
                f"${self.order.total_price:.2f}",
                classes="order-card-total",
            )
            yield Static(
                self.order.booking_date.isoformat(),
                classes="order-card-date",
            )

    @on(Click)
    def on_click(self) -> None:
        self.post_message(self.Pressed(self))
