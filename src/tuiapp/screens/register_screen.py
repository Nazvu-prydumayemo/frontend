from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Footer, Header, Static

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.forms.register_form import RegisterForm


class RegisterScreen(BaseScreen):
    """Register screen with register form."""

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(id="register-container"):
                yield Static("REGISTER", id="register-title")
                yield RegisterForm()
                yield PrimaryButton("Register", id="register")
                yield SecondaryButton("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event) -> None:
        if event.button.id == "register":
            data = self.query_one(RegisterForm).get_data()

            if not all(data.values()):
                self.toast("All fields required!")
                return

            if data["password"] != data["confirm"]:
                self.toast("Passwords don't match!")
                return

            self.toast("Successful registration!")

        elif event.button.id == "back":
            self.go_back()
