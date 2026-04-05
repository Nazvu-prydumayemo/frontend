from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, Label, Static

from tuiapp.widgets.buttons import SecondaryButton
from tuiapp.widgets.modals.base_modal import BaseModal


class PasswordHintsModal(BaseModal):
    """Modal displaying password requirements."""

    def compose_modal(self) -> ComposeResult:
        yield Static("Password Requirements", id="modal-title")
        yield Label(
            "• At least 8 characters\n"
            "• One uppercase letter\n"
            "• One lowercase letter\n"
            "• One number\n"
            "• One special character (@$!%*?&)",
            id="modal-body",
        )
        yield SecondaryButton("Close", id="close")

    @on(Button.Pressed, "#close")
    def close(self) -> None:
        self.dismiss(False)
