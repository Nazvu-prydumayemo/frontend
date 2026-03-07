from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header

from tuiapp.api.errors import APIError
from tuiapp.screens.base import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton


class MainScreen(BaseScreen):
    """
    - Main screen that consists of Login, Register and Exit buttons
    """

    def compose(self) -> ComposeResult:
        """
        - Builds the screen
        """

        yield Header()
        yield Vertical(
            PrimaryButton("Login", id="login"),
            PrimaryButton("Register", id="register"),
            PrimaryButton("Status", id="status"),
            PrimaryButton("Exit", id="exit"),
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        - Handles button events
        """

        match event.button.id:
            case "login":
                self.toast("Login")
            case "register":
                self.toast("Register")
            case "status":
                self.run_worker(self._fetch_status, exclusive=True)
            case "exit":
                self.app.exit()

    async def _fetch_status(self) -> None:
        """
        - Fetches status without freezing UI
        """
        try:
            summary = await self.app.status.status_summary()
            self.toast(summary)
        except APIError as error:
            self.toast(f"API unreachable: {error}")
