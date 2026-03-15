from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton


class HubScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Hello User!"),
            PrimaryButton("Me", id="me"),
        )
        yield Footer()
