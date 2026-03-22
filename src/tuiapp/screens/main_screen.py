from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer

from tuiapp.api.errors import APIError
from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton
from tuiapp.widgets.header import Header
from tuiapp.widgets.modals.status_modal import StatusModal


class MainScreen(BaseScreen):
    """Main screen with navigation buttons: Login, Register, Status, and Exit."""

    def compose(self) -> ComposeResult:
        yield Header(screen_name="main")
        yield Vertical(
            PrimaryButton("Login", id="login"),
            PrimaryButton("Register", id="register"),
            PrimaryButton("Status", id="status"),
            PrimaryButton("Exit", id="exit"),
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "login":
                self.change_screen("login")
            case "register":
                self.change_screen("register")
            case "status":
                self.show_modal(
                    StatusModal(
                        on_confirm=lambda: self.run_worker(self._fetch_status, exclusive=True)
                    )
                )
            case "exit":
                self.app.exit()

    async def _fetch_status(self) -> None:
        """Fetch and display the API status without freezing the UI."""
        try:
            summary = await self.app.status.status_summary()
            self.toast(summary)
        except APIError as error:
            self.toast(f"API unreachable: {error}")