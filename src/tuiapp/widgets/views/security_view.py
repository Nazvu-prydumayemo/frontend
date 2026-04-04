from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Button, Input, Static

from tuiapp.api.account.schema import PasswordRequest
from tuiapp.widgets.buttons import DangerButton, PrimaryButton
from tuiapp.widgets.inputs import PasswordInput, PasswordValidator
from tuiapp.widgets.modals.delete_account_modal import DeleteAccountModal
from tuiapp.widgets.views.base_view import BaseView


class SecurityView(BaseView):
    """Security tab view for updating the user's password and managing account."""

    small: reactive[bool] = reactive(False)

    def compose_view(self) -> ComposeResult:
        """Compose the view with password change section and delete account button."""

        with Container(id="security-container"):
            yield Static("Change Password", id="title")

            with Vertical(classes="field password-field"):
                yield Static("Current Password", classes="field-label")
                yield PasswordInput(placeholder="Current Password", id="current-password")

            with Vertical(classes="field password-field"):
                yield Static("New Password", classes="field-label")
                yield PasswordInput(placeholder="New Password", id="new-password")

            with Vertical(classes="field password-field"):
                yield Static("Confirm New Password", classes="field-label")
                yield PasswordInput(placeholder="Confirm New Password", id="confirm-password")

            with Container(id="buttons-container"):
                yield PrimaryButton(
                    "Update Password", id="update-password", classes="action-button"
                )
                yield Static(id="span")
                yield DangerButton(
                    "Delete Account",
                    variant="error",
                    id="delete-account",
                    classes="action-button",
                )

    def watch_small(self, is_small: bool) -> None:
        try:
            buttons_container = self.query_one("#buttons-container", Container)
            buttons_container.styles.layout = "vertical" if is_small else "horizontal"
            self.query_one("#update-password", PrimaryButton).styles.width = (
                "100%" if is_small else 32
            )
            self.query_one("#delete-account", DangerButton).styles.width = (
                "100%" if is_small else 32
            )

        except NoMatches:
            pass

    def on_resize(self) -> None:
        self.small = self.size.width <= 64

    @on(Input.Submitted, "#confirm-password > .password-row > #password-field")
    @on(Button.Pressed, "#update-password")
    async def handle_update_password(self) -> None:
        """Handles the password update process by verifying new password confirmation."""
        current_password = self.query_one("#current-password", PasswordInput).value
        new_password = self.query_one("#new-password", PasswordInput).value
        confirm_password = self.query_one("#confirm-password", PasswordInput).value

        if not current_password:
            self.notify("Please enter your current password", title="Security", severity="warning")
            return

        if not new_password:
            self.notify("Please enter a new password", title="Security", severity="warning")
            return

        if not confirm_password:
            self.notify("Please confirm your new password", title="Security", severity="warning")
            return

        result = PasswordValidator().validate(confirm_password)
        if not result.is_valid:
            self.notify(result.failure_descriptions[0], title="Security", severity="warning")
            return

        if new_password != confirm_password:
            self.notify("Passwords do not match", title="Security", severity="error")
            return

        if current_password == new_password:
            self.notify(
                "New password must be different from current password",
                title="Security",
                severity="error",
            )
            return

        request = PasswordRequest(current_password=current_password, new_password=new_password)
        result = await self.app.account.change_password(request)

        if result.status != "success":
            self.notify(result.message, title="Security", severity="error")
            return

        self.notify(result.message, title="Security")

    @on(Button.Pressed, "#delete-account")
    def handle_delete_account(self) -> None:
        """Opens the Delete Account modal."""
        self.screen.show_modal(DeleteAccountModal())

    def on_view_activated(self) -> None:
        """Called when the view is activated."""
        pass

    def on_view_closed(self) -> None:
        """Called when the view is closed."""
        pass
