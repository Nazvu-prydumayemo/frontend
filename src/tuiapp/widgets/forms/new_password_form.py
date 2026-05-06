from pydantic import ValidationError
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.api.auth.schema import NewPassword
from tuiapp.widgets.inputs import PasswordInput, PasswordValidator


class NewPasswordForm(Widget):
    def compose(self) -> ComposeResult:
        with Vertical(classes="form-container"):
            with Vertical(classes="field"):
                yield Static("Password", classes="field-label")
                yield PasswordInput(placeholder="Password", id="password")
            with Vertical(id="confirm-field", classes="field"):
                yield Static("Confirm Password", classes="field-label")
                yield PasswordInput(placeholder="Confirm Password", id="confirm")

    def get_data(self) -> NewPassword | str:
        password = self.query_one("#password", PasswordInput).value
        confirm = self.query_one("#confirm", PasswordInput).value

        if not all((password, confirm)):
            return "All fields required"

        result = PasswordValidator().validate(password)
        if not result.is_valid:
            return result.failure_descriptions[0]

        if password != confirm:
            return "Passwords don't match"

        try:
            return NewPassword(new_password=password)

        except ValidationError:
            return "Invalid data provided"
