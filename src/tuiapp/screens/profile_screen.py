from textual.app import ComposeResult
from textual.widgets import TabbedContent, TabPane

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.views.base_view import BaseView


class PersonalInfoView(BaseView):
    """Personal Info tab view."""

    def compose_view(self) -> ComposeResult:
        yield from []

    def on_view_activated(self):
        pass

    def on_view_closed(self):
        pass


class SecurityView(BaseView):
    """Security tab view."""

    def compose_view(self) -> ComposeResult:
        yield from []

    def on_view_activated(self):
        pass

    def on_view_closed(self):
        pass


class ProfileScreen(BaseScreen):
    """Profile screen with tabs for Personal Info, Security and Logout."""

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Personal Info", id="personal-info"):
                yield PersonalInfoView()
            with TabPane("Security", id="security"):
                yield SecurityView()
            with TabPane("Logout", id="logout"):
                pass

    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated):
        if event.tab.id == "logout":
            self.go_back()