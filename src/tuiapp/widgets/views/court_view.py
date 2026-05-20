from typing import Any

from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static, TabbedContent, TabPane

from tuiapp.api.court.schema import Court
from tuiapp.widgets.views.base_view import BaseView


class CourtView(BaseView):
    """View that displays general information about a tennis court."""

    DEFAULT_CLASSES = "view-container"

    court: reactive[Court | None] = reactive(None)
    narrow: reactive[bool] = reactive(False)

    def compose_view(self) -> ComposeResult:
        with ScrollableContainer(id="court-scroll"):
            with Vertical(id="court-header"):
                yield Static("TITLE", id="court-title")
                yield Static("SUBTITLE", id="court-subtitle")

            with Vertical(id="court-body"):
                with Vertical(id="court-info-card"):
                    yield Static("COURT INFORMATION", id="court-info-title")

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

                with Vertical(id="court-schedules"):
                    with TabbedContent(id="tabs"):
                        with TabPane("No days"):
                            yield Static("No available days")

    def _set(self, widget_id: str, value: str) -> None:
        try:
            self.query_one(f"#{widget_id}", Static).update(value)
        except NoMatches:
            pass

    def on_resize(self) -> None:
        self.narrow = self.app.size.width < 80

    def watch_narrow(self, narrow: bool) -> None:
        self.set_class(narrow, "-narrow")

    def watch_court(self, court: Any) -> None:
        self.on_view_activated()

    def on_view_activated(self) -> None:
        court = self.court
        if court is None:
            return

        self._set("court-title", court.name)
        self._set("court-subtitle", f"📍{court.location or 'N/A'}")
        self._set("court-name", court.name)
        self._set("court-location", court.location or "N/A")
        self._set("court-surface", court.surface_type)
        self._set("court-price", f"${court.price_per_hour:.2f} / hour")
        self._set("court-facility", "Indoor" if court.is_indoor else "Outdoor")
        self._set("court-hours", court.working_hours or "N/A")

        # Fetch and display court schedules
        self.app.call_later(self._load_schedules)

    def on_view_closed(self) -> None:
        pass

    async def _load_schedules(self) -> None:
        """Fetch court schedules and populate TabPanes."""
        court = self.court
        if court is None:
            return

        response = await self.app.court.get_court_schedule(court.id)

        if response.status != "success":
            self.notify(f"Error loading schedule for {court.name}")
            return

        try:
            tabs = self.query_one("#tabs", TabbedContent)
        except NoMatches:
            return

        if response.schedule is None:
            return

        tabs.clear_panes()

        for schedule in response.schedule:
            name = schedule.day_of_week.name

            opening_str = schedule.opening_time.strftime("%I:%M %p")
            closing_str = schedule.closing_time.strftime("%I:%M %p")

            pane = TabPane(name)
            pane.compose_add_child(
                Static(
                    f"{opening_str} - {closing_str}" if opening_str else "Closed",
                    classes="schedule-content",
                )
            )
            tabs.add_pane(pane)
