from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static

from tuiapp.widgets.buttons import PrimaryButton
from tuiapp.widgets.inputs import TextInput
from tuiapp.widgets.views.base_view import BaseView


class PersonalInfoView(BaseView):
    """Personal Info tab view to edit user's personal details."""

    def compose_view(self) -> ComposeResult:
        """Compose the view with form inputs and a button to save changes."""
        
        with Vertical(classes="field"):
            yield Static("First Name", classes="field-label")
            yield TextInput(placeholder="Enter first name", id="first-name")

        with Vertical(classes="field"):
            yield Static("Last Name", classes="field-label")
            yield TextInput(placeholder="Enter last name", id="last-name")

        with Vertical(classes="field"):
            yield Static("Email Address", classes="field-label")
            yield TextInput(placeholder="Enter email", id="email", disabled=True)

        yield PrimaryButton("Save Changes", id="save-changes")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        event.stop()
        
        if event.button.id == "save-changes":
            self.handle_save_changes()

    def handle_save_changes(self) -> None:
        """Handles saving the changes made to personal information."""
        first_name = self.query_one("#first-name", TextInput).value
        last_name = self.query_one("#last-name", TextInput).value

        if not first_name or not last_name:
            self.screen.toast("Please fill in all fields")
            return

        self.screen.toast("WIP")

    def on_view_activated(self) -> None:
        """Called when the view is activated."""
        pass

    def on_view_closed(self) -> None:
        """Called when the view is closed."""
        pass