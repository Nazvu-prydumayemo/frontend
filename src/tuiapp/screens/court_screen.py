from textual import on
from textual.app import ComposeResult
from textual.events import Mount
from textual.widgets import Footer, Header

from tuiapp.api.schema import Court
from tuiapp.screens.base_screen import AuthScreen
from tuiapp.widgets.views.court_view import CourtView


class CourtScreen(AuthScreen):
    """Screen that displays information about a specific tennis court."""

    def __init__(self, court: Court, **kwargs) -> None:
        """Initialize the CourtScreen.

        Args:
            court: The Court object to display.
        """
        super().__init__(**kwargs)
        self._court = court

    @on(Mount)
    async def _auth_guard(self) -> None:
        await super()._auth_guard()
        view = self.query_one(CourtView)
        view.court = self._court
        self.call_after_refresh(view.on_view_activated)

    def compose(self) -> ComposeResult:
        yield Header()
        yield CourtView()
        yield Footer()