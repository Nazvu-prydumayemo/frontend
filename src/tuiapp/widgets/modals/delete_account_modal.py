from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.widgets import Button, Static

from tuiapp.widgets.buttons import DangerButton, SecondaryButton
from tuiapp.widgets.inputs import PasswordInput
from tuiapp.widgets.modals.base_modal import BaseModal

if TYPE_CHECKING:
    pass


class DeleteAccountModal(BaseModal):
    """Modal for confirming the deletion of the user's account."""

    def __init__(self, on_toast: Callable[[str], None], **kwargs):
        """Initialize the modal with a toast callback.
        
        Args:
            on_toast: Callback function to display toast messages.
            **kwargs: Additional keyword arguments passed to BaseModal.
        """
        super().__init__(**kwargs)
        self.on_toast = on_toast

    def compose_modal(self) -> ComposeResult:
        """Compose the modal with password inputs and buttons to confirm or cancel account deletion."""
        
        with Vertical(id="delete-account-modal"):
           
            with Center():
                yield Static("✕", id="delete-icon")
            
       
            yield Static("Delete Account", id="modal-title")
            
          
            yield Static(
                "Are you absolutely sure you wish to delete your account?",
                classes="modal-description"
            )
            
         
            with Vertical(classes="field"):
                yield Static("Password", classes="field-label")
                yield PasswordInput(placeholder="", id="password")

            with Vertical(classes="field"):
                yield Static("Confirm Password", classes="field-label")
                yield PasswordInput(placeholder="", id="confirm-password")

          
            with Horizontal(classes="modal-buttons"):
                yield SecondaryButton("Cancel", id="cancel")
                yield DangerButton("Delete Account", id="delete")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        event.stop()
        
        if event.button.id == "cancel":
            self.handle_cancel()
        elif event.button.id == "delete":
            self.handle_delete()

    def handle_cancel(self) -> None:
        """Closes the modal when the 'Cancel' button is clicked."""
        self.app.pop_screen()

    def handle_delete(self) -> None:
        """Validates passwords and deletes the account if they match."""
        password = self.query_one("#password", PasswordInput).value
        confirm_password = self.query_one("#confirm-password", PasswordInput).value

    
        if not password:
            self.on_toast("Please enter your password")
            return

        if not confirm_password:
            self.on_toast("Please confirm your password")
            return

       
        if password != confirm_password:
            self.on_toast("Passwords do not match")
            return

        
        self.on_toast("WIP")
        self.app.pop_screen()