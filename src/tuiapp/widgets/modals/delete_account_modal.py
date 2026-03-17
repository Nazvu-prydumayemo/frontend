from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.widgets import Button, Static

from tuiapp.widgets.buttons import DangerButton, SecondaryButton
from tuiapp.widgets.inputs import PasswordInput
from tuiapp.widgets.modals.base_modal import BaseModal


class DeleteAccountModal(BaseModal):
    """Modal for confirming the deletion of the user's account.
    
    This modal requires the user to enter and confirm their password
    before allowing account deletion.
    """

    def compose_modal(self) -> ComposeResult:
        """Compose the modal with password inputs and buttons to confirm or cancel account deletion."""
        
        with Vertical(id="delete-account-modal"):
            # Red X icon
            with Center():
                yield Static("✕", id="delete-icon")
            
            # Title
            yield Static("Delete Account", id="modal-title")
            
            # Description
            yield Static(
                "Are you absolutely sure you wish to delete your account?",
                classes="modal-description"
            )
            
            # Password fields
            with Vertical(classes="field"):
                yield Static("Password", classes="field-label")
                yield PasswordInput(placeholder="", id="password")

            with Vertical(classes="field"):
                yield Static("Confirm Password", classes="field-label")
                yield PasswordInput(placeholder="", id="confirm-password")

            # Buttons
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

        # Validate both fields are filled
        if not password:
            self.screen.toast("Please enter your password")
            return

        if not confirm_password:
            self.screen.toast("Please confirm your password")
            return

        # Check if passwords match
        if password != confirm_password:
            self.screen.toast("Passwords do not match")
            return

        # All validations passed - proceed with deletion (WIP)
        self.screen.toast("WIP")
        self.app.pop_screen()