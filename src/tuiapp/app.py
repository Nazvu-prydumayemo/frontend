from pathlib import Path
from typing import ClassVar

from textual.app import App

from tuiapp.api.client import APIClient
from tuiapp.api.status import StatusCheckService
from tuiapp.screens.login_screen import LoginScreen
from tuiapp.screens.main_screen import MainScreen
from tuiapp.screens.profile_screen import ProfileScreen
from tuiapp.screens.register_screen import RegisterScreen


class TUIApplication(App):
    """Root application class for the Tennis TUI."""

    def __init__(self, client: APIClient) -> None:
        """Initialize the application with an API client.

        Args:
            client: The API client for communicating with the backend.
        """
        super().__init__()
        self.status = StatusCheckService(client)

    DEFAULT_CSS_FOLDER = Path("styles")
    CSS_PATH: ClassVar = [
        DEFAULT_CSS_FOLDER / "styles.tcss",
        DEFAULT_CSS_FOLDER / "buttons.tcss",
        DEFAULT_CSS_FOLDER / "main.tcss",
        DEFAULT_CSS_FOLDER / "login.tcss",
        DEFAULT_CSS_FOLDER / "register.tcss",
        DEFAULT_CSS_FOLDER / "modals.tcss",
        DEFAULT_CSS_FOLDER / "views.tcss",
    ]
    TITLE = "Tennis App"
    SUB_TITLE = "Tennis App Local Client"

    SCREENS: ClassVar[dict] = {
        "main": MainScreen,
        "login": LoginScreen,
        "register": RegisterScreen,
        "profile": ProfileScreen,
    }

    def on_mount(self) -> None:
        """Mount the first screen when the app starts."""
        self.push_screen("main")
