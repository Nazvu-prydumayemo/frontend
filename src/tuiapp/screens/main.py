from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header

from tuiapp.screens.base import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton


class MainScreen(BaseScreen):
    """
    - Main screen that consists of Login, Register and Exit buttons
    """

    def compose(self) -> ComposeResult:
        """
        - Builds the screen
        """

        yield Header()
        yield Vertical(
            PrimaryButton("Login", id="login"),
            PrimaryButton("Register", id="register"),
            PrimaryButton("Exit", id="exit"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        - Handles button events
        """

        if event.button.id == "login":
            self.toast("Login")  # Debugging purposes
            # self.change_screen("login")

        elif event.button.id == "register":
            self.toast("Register")  # Debugging purposes
            # self.change_screen("register")

        elif event.button.id == "exit":
            self.app.exit()
