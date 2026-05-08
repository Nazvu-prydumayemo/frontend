"""Court card widget for displaying tennis court summary information."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Click
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.api.court.schema import Court

MAX_LENGTH = 24


def truncate(value: str, max_length: int = MAX_LENGTH) -> str:
    """Truncate a string with ellipsis if it exceeds max_length."""
    if len(value) <= max_length:
        return value
    return value[:max_length].rstrip() + "..."


class CourtCard(Widget):
    """A card widget displaying summary information about a tennis court."""

    DEFAULT_CLASSES = "court-card"

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

    @on(Click)
    def on_click(self) -> None:
        self.post_message(self.Pressed(self))
