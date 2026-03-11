from pathlib import Path
from typing import ClassVar

from textual.app import App

from tuiapp.api.client import APIClient
from tuiapp.api.status import StatusService
from tuiapp.screens.login_screen import LoginScreen
from tuiapp.screens.main_screen import MainScreen
from tuiapp.screens.register_screen import RegisterScreen


class TUIApplication(App):
    """
    - Root application class
    """

    def __init__(self, client: APIClient) -> None:
        super().__init__()
        self.status = StatusService(client)

    DEFAULT_CSS_FOLDER = Path("styles")
    CSS_PATH: ClassVar = [
        DEFAULT_CSS_FOLDER / "styles.tcss",
        DEFAULT_CSS_FOLDER / "buttons.tcss",
        DEFAULT_CSS_FOLDER / "main.tcss",
        DEFAULT_CSS_FOLDER / "login.tcss",
        DEFAULT_CSS_FOLDER / "register.tcss",
    ]
    TITLE = "Tennis App"
    SUB_TITLE = "Tennis App Local Client"

    SCREENS: ClassVar[dict] = {
        "main": MainScreen,
        "login": LoginScreen,
        "register": RegisterScreen,
    }

    def on_mount(self) -> None:
        """
        - Mounts first page
        """

        self.push_screen("main")
