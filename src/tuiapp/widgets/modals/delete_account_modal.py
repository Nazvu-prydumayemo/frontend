from __future__ import annotations

from typing import TYPE_CHECKING

from textual import on
from textual.containers import Center, Horizontal, Vertical
from textual.widgets import Button, Static

from tuiapp.api.account.schema import DeleteRequest, UserResult
from tuiapp.widgets.buttons import DangerButton, SecondaryButton
from tuiapp.widgets.inputs import PasswordInput
from tuiapp.widgets.modals.base_modal import BaseModal

if TYPE_CHECKING:
    from textual.app import ComposeResult


class DeleteAccountModal(BaseModal):
    """Modal for confirming the deletion of the user's account."""

    def compose_modal(self) -> ComposeResult:
        """Compose the modal with password inputs and buttons to confirm or cancel account deletion."""

        with Vertical(id="delete-account-modal"):
            with Center():
                yield Static("✕", id="delete-icon")

            yield Static("Delete Account", id="modal-title")
            yield Static(
                "Are you absolutely sure you wish to delete your account?",
                classes="modal-description",
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

    @on(Button.Pressed, "#cancel")
    def cancel(self) -> None:
        """Closes the modal when the 'Cancel' button is clicked."""
        self.app.pop_screen()

    @on(Button.Pressed, "#delete")
    async def delete(self) -> None:
        """Validates passwords and deletes the account if they match."""
        password = self.query_one("#password", PasswordInput).value
        confirm_password = self.query_one("#confirm-password", PasswordInput).value

        if not password:
            self.notify("Please enter your password", title="Security", severity="warning")
            return

        if not confirm_password:
            self.notify("Please confirm your password", title="Security", severity="warning")
            return

        if password != confirm_password:
            self.notify("Passwords do not match", title="Security", severity="error")
            return

        request = DeleteRequest(password=password)
        result: UserResult = await self.app.account.delete(request)  # type: ignore

        if result.status != "success":
            self.notify(result.message, title="Security", severity="error")
            return

        self.notify(result.message, title="Security")
        self.app.token_manager.clear_tokens()  # type: ignore
        self.app.pop_screen()
        self.app.push_screen("main")
