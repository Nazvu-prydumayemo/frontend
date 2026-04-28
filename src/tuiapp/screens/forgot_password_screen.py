from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header

from tuiapp.screens.base_screen import BaseScreen


class ForgotPasswordScreen(BaseScreen):
    BINDINGS: ClassVar[list] = [
        Binding(
            key="ctrl+b,escape",
            action="go_back",
            description="Back",
            tooltip="Go to the login screen",
        ),
    ]

    def action_go_back(self) -> None:
        self.app.switch_screen("login")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
