from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Static

from tuiapp.screens.base import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.forms.login_form import LoginFormComponent


class LoginScreen(BaseScreen):
    """Login screen with email and password form."""

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="login-container"):
                yield Static("LOGIN", id="login-title")
                yield LoginFormComponent()
                yield PrimaryButton("Login", id="login")
                yield SecondaryButton("Back", id="back")

    def on_button_pressed(self, event: PrimaryButton.Pressed) -> None:
        if event.button.id == "login":
            data = self.query_one(LoginFormComponent).get_data()
            self.toast(f"Logging in as: {data['email']}")

        elif event.button.id == "back":
            self.go_back()
