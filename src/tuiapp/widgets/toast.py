from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static

if TYPE_CHECKING:
    from textual.timer import Timer


class Toast(Widget):
    """Toast notification popup component for displaying temporary messages."""

    def __init__(self, message: str, duration: float = 3.0) -> None:
        """Initialize the toast.

        Args:
            message: The message to display in the toast.
            duration: How long to display the toast in seconds.
        """
        super().__init__()
        self.message = message
        self.duration = duration
        self.timer: Timer | None = None

    def compose(self) -> ComposeResult:
        """Compose the toast widget with the message."""
        yield Static(self.message)

    def on_mount(self) -> None:
        """Set a timer to remove the toast after the specified duration."""
        self.timer = self.set_timer(self.duration, self.remove)
