from textual import on
from textual.app import ComposeResult
from textual.events import Mount
from textual.widgets import Footer, TabbedContent, TabPane

from tuiapp.api.auth.auth_guard import AuthGuard
from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.header import Header
from tuiapp.widgets.views.personal_information_view import PersonalInfoView
from tuiapp.widgets.views.security_view import SecurityView


class ProfileScreen(AuthGuard, BaseScreen):
    """Profile screen with tabs for Personal Info, Security, and Logout."""

    @on(Mount)
    async def _auth_guard(self) -> None:
        await super()._auth_guard()
        if self.user is not None:
            view = self.query_one(PersonalInfoView)
            view.user = self.user
            view.on_view_activated()

    def compose(self) -> ComposeResult:
        yield Header(screen_name="profile")
        with TabbedContent():
            with TabPane("Personal Info", id="personal-info"):
                yield PersonalInfoView()

            with TabPane("Security", id="security"):
                yield SecurityView()

            with TabPane("Logout", id="logout"):
                pass

        yield Footer()

    @on(TabbedContent.TabActivated, "#logout")
    def logout(self) -> None:
        self.notify("I logout", title="WIP", severity="information")
