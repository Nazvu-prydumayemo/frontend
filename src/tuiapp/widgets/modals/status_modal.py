from __future__ import annotations

from typing import TYPE_CHECKING

from textual.containers import Vertical
from textual.widgets import Button, Static

from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.modals.base_modal import BaseModal

if TYPE_CHECKING:
    from collections.abc import Callable

    from textual.app import ComposeResult


class StatusModal(BaseModal):
    """Modal dialog for confirming a status check action."""

    def __init__(self, on_confirm: Callable, **kwargs):
        """
        Initialize the StatusModal.

        Args:
            on_confirm: Callback function to execute when the user confirms.
            **kwargs: Additional keyword arguments passed to BaseModal.
        """
        super().__init__(**kwargs)
        self.on_confirm = on_confirm

    def compose_modal(self) -> ComposeResult:
        """Build the modal's UI layout with message and action buttons."""
        with Vertical(id="status-modal"):
            yield Static("Are you sure you want to check the status?", id="modal-status-message")
            yield PrimaryButton("Confirm", id="confirm")
            yield SecondaryButton("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button press events from the modal's confirm/cancel buttons.

        Args:
            event: The button pressed event containing the button reference.
        """
        event.stop()
        match event.button.id:
            case "confirm":
                self.on_confirm()
                self.app.pop_screen()
            case "cancel":
                self.app.pop_screen()
