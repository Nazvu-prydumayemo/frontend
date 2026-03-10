from pathlib import Path
from typing import ClassVar

from textual.app import App

from tuiapp.api.client import APIClient
from tuiapp.api.status import StatusService
from tuiapp.screens.main import MainScreen
from tuiapp.screens.login_screen import LoginScreen


class TUIApplication(App):
    """
    - Root application class
    """

    def __init__(self, client: APIClient) -> None:
        super().__init__()
        self.status = StatusService(client)

    CSS_PATH = Path("styles") / Path("styles.tcss")
    TITLE = "Tennis App"
    SUB_TITLE = "Tennis App Local Client"

    SCREENS: ClassVar[dict] = {
        "main": MainScreen,
        "login": LoginScreen,
        # "register": RegisterScreen,
    }

    def on_mount(self) -> None:
        """
        - Mounts first page
        """

        self.push_screen("main")
