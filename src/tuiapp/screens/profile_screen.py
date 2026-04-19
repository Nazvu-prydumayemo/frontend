from typing import ClassVar

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import Mount
from textual.widgets import Footer, Header, TabbedContent, TabPane

from tuiapp.screens.base_screen import AuthScreen
from tuiapp.widgets.modals.password_hints_modal import PasswordHintsModal
from tuiapp.widgets.views.personal_information_view import PersonalInfoView
from tuiapp.widgets.views.security_view import SecurityView


class ProfileScreen(AuthScreen):
    """Profile screen with tabs for Personal Info, Security, and Logout."""

    BINDINGS: ClassVar[list[Binding]] = [
        *AuthScreen.BINDINGS,
        Binding(
            key="ctrl+g",
            action="push_hints",
            description="Password Requirements",
            tooltip="Password Requirements",
        ),
    ]

    def action_push_hints(self) -> None:
        self.show_modal(PasswordHintsModal())

    @on(Mount)
    async def _auth_guard(self) -> None:
        await super()._auth_guard()
        if self.user is not None:
            view = self.query_one(PersonalInfoView)
            view.user = self.user
            self.call_after_refresh(view.on_view_activated)

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(id="tabs"):
            with TabPane("Personal Info", id="personal-info"):
                yield PersonalInfoView()

            with TabPane("Security", id="security"):
                yield SecurityView()

        yield Footer()
