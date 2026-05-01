from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static

from tuiapp.api.schema import Court
from tuiapp.widgets.views.base_view import BaseView


class CourtView(BaseView):
    """View that displays general information about a tennis court."""

    DEFAULT_CLASSES = "view-container"

    court: reactive[Court | None] = reactive(None)

    def compose_view(self) -> ComposeResult:
        with ScrollableContainer(id="court-scroll"):
            with Vertical(id="court-header"):
                with Vertical(id="court-header-info"):
                    yield Static("", id="court-title")
                    yield Static("", id="court-subtitle")
                yield Static("", id="court-diagram")
            with Horizontal(id="court-body"):
                with Vertical(id="court-info-card"):
                    yield Static("Court Information", id="court-info-title")
                    yield Static("", classes="card-divider")
                    yield Static("Court Name", classes="info-label")
                    yield Static("", id="court-name", classes="info-value")
                    yield Static("Location", classes="info-label")
                    yield Static("", id="court-location", classes="info-value")
                    yield Static("Surface Type", classes="info-label")
                    yield Static("", id="court-surface", classes="info-value")
                    yield Static("Price", classes="info-label")
                    yield Static("", id="court-price", classes="info-value price-value")
                    yield Static("Facility Type", classes="info-label")
                    yield Static("", id="court-facility", classes="info-value")
                    yield Static("Operating Hours", classes="info-label")
                    yield Static("", id="court-hours", classes="info-value")
                with Vertical(id="court-orders-card"):
                    yield Static("WIP ORDERS", id="wip-orders")

    def _set(self, widget_id: str, value: str) -> None:
        try:
            self.query_one(f"#{widget_id}", Static).update(value)
        except NoMatches:
            pass

    def watch_court(self, court: Court | None) -> None:
        self.on_view_activated()

    def on_view_activated(self) -> None:
        court = self.court
        if court is None:
            return

        self._set("court-title", court.name)
        self._set("court-subtitle", f"📍 {court.location or 'N/A'}")
        self._set("court-name", court.name)
        self._set("court-location", court.location or "N/A")
        self._set("court-surface", court.surface_type)
        self._set("court-price", f"${court.price_per_hour:.2f} / hour")
        self._set("court-facility", "Indoor" if court.is_indoor else "Outdoor")
        self._set("court-hours", court.working_hours or "N/A")

    def on_view_closed(self) -> None:
        pass