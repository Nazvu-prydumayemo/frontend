from pydantic import ValidationError
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.api.auth.schema import ForgotPasswordRequest
from tuiapp.widgets.inputs import TextInput


class ForgotPasswordForm(Widget):
    def compose(self) -> ComposeResult:
        with Vertical(id="login-form"):
            with Vertical(classes="field"):
                yield Static("Email", classes="field-label")
                yield TextInput(placeholder="example@email.com", id="email")

    def get_data(self) -> ForgotPasswordRequest | str:
        email = self.query_one("#email", TextInput).value
        if not email:
            return "All fields required"

        try:
            return ForgotPasswordRequest(email=email)

        except ValidationError:
            return "Invalid email format"
