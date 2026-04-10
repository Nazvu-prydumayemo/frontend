from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Static

from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.modals.base_modal import BaseModal


class ConfirmationModal(BaseModal):
    def __init__(self, action: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self._action = action

    def compose_modal(self) -> ComposeResult:
        yield Static(f"Are you sure you want to {self._action}?", id="modal-title")
        with Container(id="buttons-container"):
            yield PrimaryButton("Confirm", variant="success", id="action")
            yield SecondaryButton("Cancel", variant="warning", id="close")

    @on(Button.Pressed, "#close")
    def close(self) -> None:
        self.dismiss(False)

    @on(Button.Pressed, "#action")
    def action(self) -> None:
        self.dismiss(True)
