from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.widgets.inputs import PasswordInput, TextInput


class RegisterForm(Widget):
    """Registration form with name, email, password, and confirmation fields."""

    def compose(self) -> ComposeResult:
        with Vertical(id="form"):
            with Vertical(classes="field"):
                yield Static("Name and Lastname", classes="field-label")
                yield TextInput(placeholder="Name Lastname", id="name")

            with Vertical(classes="field"):
                yield Static("Email", classes="field-label")
                yield TextInput(placeholder="example@email.com", id="email")

            with Vertical(classes="field"):
                yield Static("Password", classes="field-label")
                yield PasswordInput(placeholder="Password", id="password")

            with Vertical(classes="field"):
                yield Static("Confirm Password", classes="field-label")
                yield PasswordInput(placeholder="Confirm Password", id="confirm")

    def get_data(self) -> dict[str, str]:
        """Get the form data.

        Returns:
            A dictionary with name, email, password, and confirm values.
        """
        return {
            "name": self.query_one("#name", TextInput).value,
            "email": self.query_one("#email", TextInput).value,
            "password": self.query_one("#password", PasswordInput).value,
            "confirm": self.query_one("#confirm", PasswordInput).value,
        }