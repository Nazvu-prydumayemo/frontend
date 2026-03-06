from typing import TYPE_CHECKING

from textual.screen import Screen

from tuiapp.widgets.toast import Toast

if TYPE_CHECKING:
    from tuiapp.app import TUIApplication


class BaseScreen(Screen):
    """
    - Base Class for all screens
    - All screens should be derived from this
    """

    if TYPE_CHECKING:
        app: "TUIApplication"

    def toast(self, message: str, duration: float = 3.0) -> None:
        """
        - Creates a toast popup with the given message
        """
        self.mount(Toast(message, duration))

    def change_screen(self, screen: str) -> None:
        """
        - Switches screen to given
        """

        self.app.push_screen(screen)

    def go_back(self) -> None:
        """
        - Switches to previous screen
        """
        self.app.pop_screen()
