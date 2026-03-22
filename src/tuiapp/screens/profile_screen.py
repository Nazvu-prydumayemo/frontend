from textual import on
from textual.app import ComposeResult
from textual.widgets import Footer, TabbedContent, TabPane

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.header import Header
from tuiapp.widgets.views.personal_information_view import PersonalInfoView
from tuiapp.widgets.views.security_view import SecurityView


class ProfileScreen(BaseScreen):
    """Profile screen with tabs for Personal Info, Security, and Logout."""

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
        self.toast("I logout")  # Placeholder for now, because logout can't be used as a button?