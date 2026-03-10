from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.widgets.inputs import PasswordInput, TextInput


class LoginFormComponent(Widget):
    """Login form component with email and password fields."""

    def compose(self) -> ComposeResult:
        with Vertical(id="form"):
            with Vertical(classes="field"):
                yield Static("Email", classes="field-label")
                yield TextInput(placeholder="example@email.com", id="email")

            with Vertical(classes="field"):
                yield Static("Password", classes="field-label")
                yield PasswordInput(id="password")

    def get_data(self) -> dict:
        """Returns email and password from the form."""
        return {
            "email": self.query_one("#email").value,
            "password": self.query_one("#password").value,
        }