from typing import ClassVar

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton
from tuiapp.widgets.modals.confirmation_modal import ConfirmationModal


class MainScreen(BaseScreen):
    """Main screen with navigation buttons: Login, Register, Status, and Exit."""

    BINDINGS: ClassVar[list[Binding]] = [
        Binding("ctrl+b,esc", "exit", "Exit", tooltip="Close the application")
    ]

    heading = r"""
███╗   ██╗██████╗    ████████╗███████╗███╗   ██╗███╗   ██╗██╗███████╗
████╗  ██║██╔══██╗   ╚══██╔══╝██╔════╝████╗  ██║████╗  ██║██║██╔════╝
██╔██╗ ██║██████╔╝█████╗██║   █████╗  ██╔██╗ ██║██╔██╗ ██║██║███████╗
██║╚██╗██║██╔═══╝ ╚════╝██║   ██╔══╝  ██║╚██╗██║██║╚██╗██║██║╚════██║
██║ ╚████║██║           ██║   ███████╗██║ ╚████║██║ ╚████║██║███████║
╚═╝  ╚═══╝╚═╝           ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝╚══════╝"""

    heading_status: reactive[bool] = reactive(True)

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="main-container"):
            yield Static(self.heading, id="heading")
            with Container(id="button-container"):
                yield PrimaryButton("Login", variant="primary", id="login")
                yield PrimaryButton("Signup", variant="primary", id="register")
        yield Footer()

    def watch_heading_status(self, show_large: bool) -> None:
        try:
            self.query_one("#heading", Static).display = show_large

        except NoMatches:
            pass

    def on_resize(self) -> None:
        self.heading_status = self.size.width >= 70

    @on(Button.Pressed, "#login")
    def login(self) -> None:
        self.app.switch_screen("login")

    @on(Button.Pressed, "#register")
    def register(self) -> None:
        self.app.switch_screen("register")

    def _check_quit(self, quit: bool | None) -> None:
        if quit:
            self.app.exit()

    def action_exit(self) -> None:
        self.show_modal(ConfirmationModal("Exit"), self._check_quit)
