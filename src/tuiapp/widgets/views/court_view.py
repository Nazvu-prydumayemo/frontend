"""View that displays detailed information about a tennis court."""

from datetime import date
from typing import Any

from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Button, Static, TabbedContent, TabPane

from tuiapp.api.court.schema import Court
from tuiapp.api.order.schema import OrderRequest
from tuiapp.time_utils import utc_to_local
from tuiapp.widgets.buttons import PrimaryButton
from tuiapp.widgets.courts.schedule_slot import ScheduleSlot
from tuiapp.widgets.modals.confirmation_modal import ConfirmationModal
from tuiapp.widgets.views.base_view import BaseView


class CourtView(BaseView):
    """View that displays general information about a tennis court."""

    DEFAULT_CLASSES = "view-container"

    court: reactive[Court | None] = reactive(None)
    narrow: reactive[bool] = reactive(False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_slot_ids: set[int] = set()

    def compose_view(self) -> ComposeResult:
        """Build the court detail view with header, info card, schedule tabs, and booking controls."""
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
                    with TabbedContent(id="schedule-tabs"):
                        with TabPane("No days"):
                            yield Static("No available days")

                with Vertical(id="court-schedules"):
                    with TabbedContent(id="slot-tabs"):
                        with TabPane("No days"):
                            yield Static("No available days")

                    yield PrimaryButton(
                        "Order Selected Slots", variant="primary", id="order-button"
                    )

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

        # Fetch and display court schedules
        self.app.call_later(self._load_schedules)
        self.app.call_later(self._load_slots)

    def on_view_closed(self) -> None:
        self.selected_slot_ids.clear()

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
            tabs = self.query_one("#schedule-tabs", TabbedContent)
        except NoMatches:
            return

        if response.schedule is None:
            return

        tabs.clear_panes()

        for schedule in response.schedule:
            name = schedule.day_of_week.name

            if schedule.opening_time is None or schedule.closing_time is None:
                continue

            opening_str = utc_to_local(schedule.opening_time).strftime("%H:%M")
            closing_str = utc_to_local(schedule.closing_time).strftime("%H:%M")

            pane = TabPane(name)
            pane.compose_add_child(
                Static(
                    f"{opening_str} - {closing_str}" if opening_str else "Closed",
                    classes="schedule-content",
                )
            )
            tabs.add_pane(pane)

    async def _load_slots(self) -> None:
        court = self.court
        if court is None:
            return

        self.selected_slot_ids.clear()

        try:
            slot_tabs = self.query_one("#slot-tabs", TabbedContent)
        except NoMatches:
            return

        slot_tabs.clear_panes()

        today = date.today()

        for day_offset in range(7):
            query_date = (
                date(today.year, today.month, today.day + day_offset)
                if False
                else date.fromordinal(today.toordinal() + day_offset)
            )

            response = await self.app.court.get_court_available_slots(court.id, query_date)

            if response.status != "success" or response.slots is None:
                continue

            if response.slots.total_slots == 0:
                continue

            tab_label = query_date.strftime("%a %b %d")
            pane = TabPane(tab_label)

            for slot in response.slots.available_slots:
                pane.compose_add_child(ScheduleSlot(slot))

            slot_tabs.add_pane(pane)

    @on(ScheduleSlot.Selected)
    def on_schedule_slot_selected(self, event: ScheduleSlot.Selected) -> None:
        event.stop()
        self.selected_slot_ids.add(event.slot_id)

    @on(ScheduleSlot.Deselected)
    def on_schedule_slot_deselected(self, event: ScheduleSlot.Deselected) -> None:
        event.stop()
        self.selected_slot_ids.discard(event.slot_id)

    @on(Button.Pressed, "#order-button")
    def on_order_button_pressed(self) -> None:
        if not self.selected_slot_ids:
            self.notify("No slots selected", title="Order")
            return

        self.app.push_screen(
            ConfirmationModal("book the selected slots"),
            self._handle_order_confirmation,
        )

    async def _handle_order_confirmation(self, confirmed: bool | None) -> None:
        if not confirmed or self.court is None:
            return

        if not self.selected_slot_ids:
            self.notify("No slots selected", title="Order", severity="warning")
            return

        request = OrderRequest(
            court_id=self.court.id,
            booking_slot_ids=list(self.selected_slot_ids),
        )

        result = await self.app.order.create_order(request)

        if result.status == "success" and result.order is not None:
            self.selected_slot_ids.clear()
            self.notify("Thank you for the order!", title="Order")
            await self._load_slots()

        else:
            self.notify(result.message, title="Order", severity="error")

    @on(TabbedContent.TabActivated, "#slot-tabs")
    def on_slot_tab_changed(self) -> None:
        self.selected_slot_ids.clear()
        for slot in self.query(ScheduleSlot):
            slot.pressed = False
