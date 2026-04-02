from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton


class MainScreen(BaseScreen):
    """Main screen with navigation buttons: Login, Register, Status, and Exit."""

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
                yield PrimaryButton("Login", id="login")
                yield PrimaryButton("Signup", id="register")
                yield SecondaryButton("Exit", id="exit")
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
        self.change_screen("login")

    @on(Button.Pressed, "#register")
    def register(self) -> None:
        self.change_screen("register")

    @on(Button.Pressed, "#exit")
    def exit(self) -> None:
        self.app.exit()
