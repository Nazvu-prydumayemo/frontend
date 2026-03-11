from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Footer, Header, Static

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.forms.login_form import LoginForm


class LoginScreen(BaseScreen):
    """Login screen with email and password form."""

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(id="login-container"):
                yield Static("LOGIN", id="login-title")
                yield LoginForm()
                yield PrimaryButton("Login", id="login")
                yield SecondaryButton("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: PrimaryButton.Pressed) -> None:
        if event.button.id == "login":
            data = self.query_one(LoginForm).get_data()

            if not all(data.values()):
                self.toast("All fields required!")
                return

            self.toast(f"Logging in as: {data['email']}")

        elif event.button.id == "back":
            self.go_back()
