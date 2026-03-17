from textual.app import ComposeResult
from textual.widgets import TabbedContent, TabPane

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.views.personal_information_view import PersonalInfoView
from tuiapp.widgets.views.security_view import SecurityView
from tuiapp.widgets.views.base_view import BaseView


class ProfileScreen(BaseScreen):
    """Profile screen with tabs for Personal Info, Security, and Logout."""

    def compose(self) -> ComposeResult:
        with TabbedContent():
           
            with TabPane("Personal Info", id="personal-info"):
                yield PersonalInfoView()

            
            with TabPane("Security", id="security"):
                yield SecurityView()

            
            with TabPane("Logout", id="logout"):
                pass

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated):
        """Handling tab activation. If 'Logout', then go back."""
        if event.tab.id == "logout":
            self.go_back()