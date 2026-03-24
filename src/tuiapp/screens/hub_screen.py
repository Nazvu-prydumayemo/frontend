"""Hub screen - the main authenticated user dashboard."""

from textual.app import ComposeResult
from textual.widgets import Footer

from tuiapp.api.auth.auth_guard import AuthGuard
from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.header import Header


class HubScreen(AuthGuard, BaseScreen):  # type: ignore
    """Main dashboard screen displayed after successful authentication.

    Provides access to user-specific features and information.
    """

    def compose(self) -> ComposeResult:
        yield Header(screen_name="hub")
        yield Footer()
