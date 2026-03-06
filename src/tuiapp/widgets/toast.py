from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static

if TYPE_CHECKING:
    from textual.timer import Timer


class Toast(Widget):
    """
    - Popup Toast component for notifications
    """

    def __init__(self, message: str, duration: float = 3.0) -> None:
        super().__init__()
        self.message = message
        self.duration = duration
        self.timer: Timer | None = None

    def compose(self) -> ComposeResult:
        """
        - Builds the popup
        """

        yield Static(self.message)

    def on_mount(self) -> None:
        """
        - Removes the popup after some time
        """

        self.timer = self.set_timer(self.duration, self.remove)
