"""Hub screen - the main authenticated user dashboard."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Static

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton


class HubScreen(BaseScreen):
    """Main dashboard screen displayed after successful authentication.

    Provides access to user-specific features and information.
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Hello User!"),
            PrimaryButton("Me", id="me"),
        )
        yield Footer()

    @on(Button.Pressed, "#me")
    async def me(self) -> None:
        status: str = await self.app.auth.me()
        self.toast(status)
