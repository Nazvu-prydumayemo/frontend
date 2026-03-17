from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static

from tuiapp.widgets.buttons import DangerButton, PrimaryButton
from tuiapp.widgets.inputs import PasswordInput
from tuiapp.widgets.modals.delete_account_modal import DeleteAccountModal
from tuiapp.widgets.views.base_view import BaseView


class SecurityView(BaseView):
    """Security tab view for updating the user's password and managing account."""

    def compose_view(self) -> ComposeResult:
        """Compose the view with password change section and delete account button."""
        
        # Change Password Section
        yield Static("Change Password", classes="section-title")
        
        with Vertical(classes="field"):
            yield Static("Current Password", classes="field-label")
            yield PasswordInput(placeholder="Current Password", id="current-password")

        with Vertical(classes="field"):
            yield Static("New Password", classes="field-label")
            yield PasswordInput(placeholder="New Password", id="new-password")

        with Vertical(classes="field"):
            yield Static("Confirm New Password", classes="field-label")
            yield PasswordInput(placeholder="Confirm New Password", id="confirm-password")

        yield PrimaryButton("Update Password", id="update-password")

        # Delete Account Section
        yield Static("Delete Account", classes="danger-title")
        yield Static(
            "Once you delete your account, there is no going back. Please be certain.",
            classes="danger-warning"
        )
        yield DangerButton("Delete Account", id="delete-account")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        event.stop()
        
        if event.button.id == "update-password":
            self.handle_update_password()
        elif event.button.id == "delete-account":
            self.handle_delete_account()

    def handle_update_password(self) -> None:
        """Handles the password update process by verifying new password confirmation."""
        current_password = self.query_one("#current-password", PasswordInput).value
        new_password = self.query_one("#new-password", PasswordInput).value
        confirm_password = self.query_one("#confirm-password", PasswordInput).value

        if not current_password:
            self.screen.toast("Please enter your current password")
            return

        if not new_password:
            self.screen.toast("Please enter a new password")
            return

        if not confirm_password:
            self.screen.toast("Please confirm your new password")
            return

        if new_password != confirm_password:
            self.screen.toast("Passwords do not match")
            return

        if current_password == new_password:
            self.screen.toast("New password must be different from current password")
            return

        self.screen.toast("WIP")

    def handle_delete_account(self) -> None:
        """Opens the Delete Account modal."""
        self.screen.show_modal(DeleteAccountModal(on_toast=self.screen.toast))

    def on_view_activated(self) -> None:
        """Called when the view is activated."""
        pass

    def on_view_closed(self) -> None:
        """Called when the view is closed."""
        pass