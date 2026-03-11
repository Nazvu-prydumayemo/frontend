from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.widgets.inputs import PasswordInput, TextInput


class LoginForm(Widget):
    """Login form with email and password input fields."""

    def compose(self) -> ComposeResult:
        with Vertical(id="form"):
            with Vertical(classes="field"):
                yield Static("Email", classes="field-label")
                yield TextInput(placeholder="example@email.com", id="email")

            with Vertical(classes="field"):
                yield Static("Password", classes="field-label")
                yield PasswordInput(placeholder="Password", id="password")

    def get_data(self) -> dict[str, str]:
        """Get the form data.

        Returns:
            A dictionary with email and password values.
        """
        return {
            "email": self.query_one("#email", TextInput).value,
            "password": self.query_one("#password", PasswordInput).value,
        }
