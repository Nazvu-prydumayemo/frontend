"""Court card widget for displaying tennis court summary information."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

MAX_LENGTH = 24


def truncate(value: str, max_length: int = MAX_LENGTH) -> str:
    """Truncate a string with ellipsis if it exceeds max_length."""
    if len(value) <= max_length:
        return value
    return value[:max_length].rstrip() + "..."


class CourtCard(Widget):
    """A card widget displaying summary information about a tennis court."""

    DEFAULT_CLASSES = "court-card"

    def __init__(
        self,
        name: str,
        location: str,
        price: str,
        court_type: str,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._name = truncate(name)
        self._location = truncate(location)
        self._price = truncate(price)
        self._court_type = truncate(court_type)

    def compose(self) -> ComposeResult:
        with Vertical(classes="court-card-body"):
            yield Static(self._name, classes="court-card-name")
            yield Static(self._location, classes="court-card-location")
            yield Static(self._price, classes="court-card-price")
            yield Static(self._court_type, classes="court-card-type")