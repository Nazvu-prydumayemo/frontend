from pydantic import ValidationError
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.api.auth.schema import RegisterRequest
from tuiapp.widgets.inputs import PasswordInput, TextInput


class RegisterForm(Widget):
    """Registration form with name, email, password, and confirmation fields."""

    def compose(self) -> ComposeResult:
        with Vertical(id="form"):
            with Vertical(classes="field"):
                yield Static("Firstname", classes="field-label")
                yield TextInput(placeholder="Firstname", id="firstname")

            with Vertical(classes="field"):
                yield Static("Lastname", classes="field-label")
                yield TextInput(placeholder="Lastname", id="lastname")

            with Vertical(classes="field"):
                yield Static("Email", classes="field-label")
                yield TextInput(placeholder="example@email.com", id="email")

            with Vertical(classes="field"):
                yield Static("Password", classes="field-label")
                yield PasswordInput(placeholder="Password", id="password")

            with Vertical(classes="field"):
                yield Static("Confirm Password", classes="field-label")
                yield PasswordInput(placeholder="Confirm Password", id="confirm")

    def get_data(self) -> RegisterRequest | str:
        """Get the form data.

        Returns:
            A pydantic model with firstname, lastname, email and password values or string error if invalid data was provided.
        """
        firstname = self.query_one("#firstname", TextInput).value
        lastname = self.query_one("#lastname", TextInput).value
        email = self.query_one("#email", TextInput).value
        password = self.query_one("#password", PasswordInput).value
        confirm = self.query_one("#confirm", PasswordInput).value

        if not all((firstname, lastname, email, password, confirm)):
            return "All fields required"

        if password != confirm:
            return "Passwords don't match"

        try:
            return RegisterRequest(
                firstname=firstname, lastname=lastname, email=email, password=password
            )

        except ValidationError:
            return "Invalid email format"
