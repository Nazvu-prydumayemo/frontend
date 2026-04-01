from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton


class MainScreen(BaseScreen):
    """Main screen with navigation buttons: Login, Register, Status, and Exit."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            PrimaryButton("Login", id="login"),
            PrimaryButton("Register", id="register"),
            SecondaryButton("Exit", id="exit"),
        )
        yield Footer()

    @on(Button.Pressed, "#login")
    def login(self) -> None:
        self.change_screen("login")

    @on(Button.Pressed, "#register")
    def register(self) -> None:
        self.change_screen("register")

    @on(Button.Pressed, "#exit")
    def exit(self) -> None:
        self.app.exit()
