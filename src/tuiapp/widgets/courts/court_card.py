"""Court card widget for displaying tennis court summary information."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Click, Resize
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.api.court.schema import Court

MAX_LENGTH = 20
SMALL_WIDTH_THRESHOLD = 24


def truncate(value: str, max_length: int = MAX_LENGTH) -> str:
    """Truncate a string with ellipsis if it exceeds max_length."""
    if len(value) <= max_length:
        return value
    return value[:max_length].rstrip() + "..."


class CourtCard(Widget):
    """A card widget displaying summary information about a tennis court."""

    DEFAULT_CLASSES = "court-card"

    selected: reactive[bool] = reactive(False)
    small: reactive[bool] = reactive(False)

    def watch_selected(self, value: bool) -> None:
        self.set_class(value, "selected")

    def watch_small(self, value: bool) -> None:
        self.set_class(value, "small")
        self._refresh_content()

    class Pressed(Message):
        """Posted when the court card is clicked."""

        def __init__(self, court_card: "CourtCard") -> None:
            super().__init__()
            self.court_card = court_card

    def __init__(
        self,
        court: Court,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.court = court

    def compose(self) -> ComposeResult:
        with Vertical(classes="court-card-body"):
            yield Static(
                f"{truncate(self.court.name)}",
                classes="court-card-compact",
            )
            yield Static(
                f"{truncate(self.court.name)} ${self.court.price_per_hour}/h",
                classes="court-card-name",
            )
            yield Static(
                truncate(self.court.location) if self.court.location else "N/A",
                classes="court-card-location",
            )
            yield Static(
                f"{'Indoor' if self.court.is_indoor else 'Outdoor'} {self.court.surface_type}",
                classes="court-card-type",
            )

    def _refresh_content(self) -> None:
        is_small = self.small
        self.query_one(".court-card-compact", Static).display = is_small
        self.query_one(".court-card-name", Static).display = not is_small
        self.query_one(".court-card-location", Static).display = not is_small
        self.query_one(".court-card-type", Static).display = not is_small

    def on_mount(self) -> None:
        self._refresh_content()

    def on_resize(self, event: Resize) -> None:
        self.small = event.size.width < SMALL_WIDTH_THRESHOLD

    @on(Click)
    def on_click(self) -> None:
        self.post_message(self.Pressed(self))
