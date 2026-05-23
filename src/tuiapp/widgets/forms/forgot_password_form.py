"""Form for requesting a password reset via email."""

from pydantic import ValidationError
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from tuiapp.api.auth.schema import ForgotPasswordRequest
from tuiapp.widgets.forms.base_form import BaseForm
from tuiapp.widgets.inputs import TextInput


class ForgotPasswordForm(BaseForm):
    """Form for requesting a password reset by entering an email address."""

    def compose(self) -> ComposeResult:
        with Vertical(classes="form-container"):
            with Vertical(classes="field"):
                yield Static("Email", classes="field-label")
                yield TextInput(placeholder="example@email.com", id="email")

    def get_data(self) -> ForgotPasswordRequest | str:
        """Get the form data.

        Returns:
            A pydantic model with email value or string error if invalid data was provided.
        """
        email = self.query_one("#email", TextInput).value
        if not email:
            return "All fields required"

        try:
            return ForgotPasswordRequest(email=email)

        except ValidationError:
            return "Invalid email format"
