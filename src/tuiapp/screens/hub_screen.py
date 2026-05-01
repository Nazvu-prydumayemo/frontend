"""Hub screen - the main authenticated user dashboard."""

from textual.app import ComposeResult
from textual.widgets import Footer, Header

from tuiapp.screens.base_screen import AuthScreen


class HubScreen(AuthScreen):
    """Main dashboard screen displayed after successful authentication."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()