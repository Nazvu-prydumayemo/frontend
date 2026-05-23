"""View that displays detailed information about an order."""

from typing import Any

from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from tuiapp.api.order.schema import OrderDetail
from tuiapp.widgets.views.base_view import BaseView


class OrderView(BaseView):
    """View that displays detailed information about an order."""

    DEFAULT_CLASSES = "view-container"

    order: reactive[OrderDetail | None] = reactive(None)
    court_name: reactive[str | None] = reactive(None)
    booking_time_range: reactive[str | None] = reactive(None)
    narrow: reactive[bool] = reactive(False)

    def compose_view(self) -> ComposeResult:
        """Build the order detail view with header and order information card."""
        with ScrollableContainer(id="order-scroll"):
            with Vertical(id="order-header"):
                yield Static("TITLE", id="order-title")
                yield Static("SUBTITLE", id="order-subtitle")

            with Vertical(id="order-body"):
                with Vertical(id="order-info-card"):
                    yield Static("ORDER INFORMATION", id="order-info-title")

                    yield Static("Court", classes="info-label")
                    yield Static("", id="order-court-name", classes="info-value")

                    yield Static("Booking Date", classes="info-label")
                    yield Static("", id="order-booking-date", classes="info-value")

                    yield Static("Total Price", classes="info-label")
                    yield Static("", id="order-total-price", classes="info-value price-value")

                    yield Static("Booking Time", classes="info-label")
                    yield Static("", id="order-booking-time", classes="info-value")

    def _set(self, widget_id: str, value: str) -> None:
        try:
            self.query_one(f"#{widget_id}", Static).update(value)
        except NoMatches:
            pass

    def on_resize(self) -> None:
        self.narrow = self.app.size.width < 80

    def watch_narrow(self, narrow: bool) -> None:
        self.set_class(narrow, "-narrow")

    def watch_order(self, order: Any) -> None:
        self.on_view_activated()

    def watch_court_name(self, name: str | None) -> None:
        self._set("order-court-name", name or "Loading...")

    def watch_booking_time_range(self, value: str | None) -> None:
        self._set("order-booking-time", value or "")

    def on_view_activated(self) -> None:
        order = self.order
        if order is None:
            return

        self._set("order-title", f"Order #{order.id}")
        self._set("order-subtitle", f"${order.total_price:.2f}")
        self._set("order-court-name", self.court_name or "Loading...")
        self._set("order-booking-date", order.booking_date.isoformat())
        self._set("order-total-price", f"${order.total_price:.2f}")
        self._set("order-booking-time", self.booking_time_range or "")

    def on_view_closed(self) -> None:
        pass
