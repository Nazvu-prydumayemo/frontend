from pydantic import ValidationError
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.api.auth.schema import LoginRequest
from tuiapp.widgets.inputs import EmailInput, PasswordInput


class LoginForm(Widget):
    """Login form with email and password input fields."""

    def compose(self) -> ComposeResult:
        with Vertical(id="form"):
            with Vertical(classes="field"):
                yield Static("Email", classes="field-label")
                yield EmailInput(placeholder="example@email.com", id="email")

            with Vertical(classes="field"):
                yield Static("Password", classes="field-label")
                yield PasswordInput(placeholder="Password", id="password")

    def get_data(self) -> LoginRequest | str:
        """Get the form data.

        Returns:
            A pydantic model with email and password values or string error if invalid data was provided.
        """
        email = self.query_one("#email", EmailInput).value
        password = self.query_one("#password", PasswordInput).value
        if not email or not password:
            return "All fields required"

        try:
            return LoginRequest(email=email, password=password)

        except ValidationError:
            return "Invalid email format"