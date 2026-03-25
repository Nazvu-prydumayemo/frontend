from collections.abc import Iterable
from pathlib import Path
from typing import ClassVar

from textual.app import App, SystemCommand, get_system_commands_provider
from textual.screen import Screen

from tuiapp.api.auth.auth import AuthService
from tuiapp.api.auth.token_manager import TokenManagerService
from tuiapp.api.client import APIClient
from tuiapp.api.status.status import StatusService
from tuiapp.screens.hub_screen import HubScreen
from tuiapp.screens.login_screen import LoginScreen
from tuiapp.screens.main_screen import MainScreen
from tuiapp.screens.profile_screen import ProfileScreen
from tuiapp.screens.register_screen import RegisterScreen


class TUIApplication(App):
    """Root application class for the Tennis TUI."""

    def __init__(self, client: APIClient, token_manager: TokenManagerService) -> None:
        """Initialize the application with an API client.

        Args:
            client: The API client for communicating with the backend.
        """
        super().__init__()
        self.client = client
        self.token_manager = token_manager

        self.status = StatusService(self.client)
        self.auth = AuthService(self.client)

    DEFAULT_CSS_FOLDER = Path("styles")
    CSS_PATH: ClassVar = [
        DEFAULT_CSS_FOLDER / "styles.tcss",
        DEFAULT_CSS_FOLDER / "buttons.tcss",
        DEFAULT_CSS_FOLDER / "main.tcss",
        DEFAULT_CSS_FOLDER / "login.tcss",
        DEFAULT_CSS_FOLDER / "register.tcss",
        DEFAULT_CSS_FOLDER / "modals.tcss",
        DEFAULT_CSS_FOLDER / "views.tcss",
        DEFAULT_CSS_FOLDER / "header.tcss",
    ]
    TITLE = "Tennis App"
    SUB_TITLE = "Tennis App Local Client"

    SCREENS: ClassVar[dict] = {
        "main": MainScreen,
        "login": LoginScreen,
        "register": RegisterScreen,
        "profile": ProfileScreen,
        "hub": HubScreen,
    }
    COMMANDS: ClassVar = {get_system_commands_provider}

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)

    async def on_mount(self) -> None:
        """Mount the first screen when the app starts."""
        session = await self.token_manager.refresh_access_token()
        if not session:
            self.push_screen("main")
            return

        self.push_screen("hub")
