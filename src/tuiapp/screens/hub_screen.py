"""Hub screen - the main authenticated user dashboard."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.events import Mount
from textual.widgets import Footer, Header

from tuiapp.screens.base_screen import AuthScreen
from tuiapp.widgets.views.court_view import CourtView


class HubScreen(AuthScreen):
    """Main dashboard screen displayed after successful authentication."""

    @on(Mount)
    async def _auth_guard(self) -> None:
        await super()._auth_guard()

    @on(Mount)
    async def _auth_guard(self) -> None:
        await super()._auth_guard()

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="hub-container"):
            # TODO: REPLACE WITH THE ACTUAL COURT LIST
            yield ScrollableContainer(id="court-list")
            yield CourtView()
        yield Footer()
