from __future__ import annotations

from typing import TYPE_CHECKING

from textual.screen import Screen

from tuiapp.widgets.toast import Toast


class BaseScreen(Screen):
    """Base screen class. All screens should inherit from this."""

    if TYPE_CHECKING:
        app: TUIApplication  # type: ignore # noqa: F821

    def toast(self, message: str, duration: float = 3.0) -> None:
        """Display a toast notification popup.

        Args:
            message: The message to display in the toast.
            duration: How long to display the toast in seconds.
        """
        self.mount(Toast(message, duration))

    def change_screen(self, screen: str) -> None:
        """Navigate to a new screen by pushing it onto the stack.

        Args:
            screen: The name of the screen to navigate to.
        """
        self.app.push_screen(screen)

    def go_back(self) -> None:
        """Return to the previous screen by popping the current screen."""
        self.app.pop_screen()
