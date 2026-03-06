from pathlib import Path
from typing import ClassVar

from textual.app import App

from tuiapp.screens.main import MainScreen


class TUIApplication(App):
    """
    - Root application class
    """

    CSS_PATH = Path("styles") / Path("styles.tcss")
    TITLE = "Tennis App"
    SUB_TITLE = "Tennis App Local Client"

    SCREENS: ClassVar[dict] = {
        "main": MainScreen,
        # "login": LoginScreen,
        # "register": RegisterScreen,
    }

    def on_mount(self) -> None:
        """
        - Mounts first page
        """

        self.push_screen("main")


if __name__ == "__main__":
    TUIApplication().run()
