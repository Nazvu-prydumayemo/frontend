from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Vertical

from widgets.login_inputs import TextInput, PasswordInput
from widgets.login_buttons import PrimaryButton, SecondaryButton


class LoginFormComponent(Static):
    """Login form component with email, password fields and action buttons."""

    def compose(self) -> ComposeResult:
        with Vertical(id="form-container"):
            yield Static("Email", classes="field-label")
            yield TextInput(placeholder="example@email.com", id="email")

            yield Static("Password", classes="field-label")
            yield PasswordInput(placeholder="Password", id="password")

            yield PrimaryButton("Login", id="login")
            yield SecondaryButton("Back", id="back")