"""Hub screen - the main authenticated user dashboard."""

from textual import on
from textual.app import ComposeResult
from textual.events import Mount
from textual.widgets import Footer, Header

from tuiapp.screens.base_screen import AuthScreen


class HubScreen(AuthScreen):
    """Main dashboard screen displayed after successful authentication.

    Provides access to user-specific features and information.
    """

    @on(Mount)
    async def _auth_guard(self) -> None:
        await super()._auth_guard()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
