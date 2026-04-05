from typing import TYPE_CHECKING

from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Button, Static

from tuiapp.api.account.schema import ProfileRequest
from tuiapp.widgets.buttons import PrimaryButton
from tuiapp.widgets.inputs import TextInput
from tuiapp.widgets.views.base_view import BaseView

if TYPE_CHECKING:
    from tuiapp.api.account.schema import User


class PersonalInfoView(BaseView):
    """Personal Info tab view to edit user's personal details."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.user: User | None = None

    small: reactive[bool] = reactive(False)

    def compose_view(self) -> ComposeResult:
        with ScrollableContainer(id="personal-info-container"):
            with Vertical(classes="field"):
                yield Static("First Name", classes="field-label")
                yield TextInput(id="first-name")

            with Vertical(classes="field"):
                yield Static("Last Name", classes="field-label")
                yield TextInput(id="last-name")

            with Vertical(classes="field", id="email-field"):
                yield Static("Email Address", classes="field-label")
                yield TextInput(id="email", disabled=True)

            yield PrimaryButton("Save Changes", id="save-changes")

    def watch_small(self, is_small: bool) -> None:
        try:
            form = self.query_one("#personal-info-container", ScrollableContainer)
            form.styles.grid_size_columns = 1 if is_small else 2
            form.styles.grid_size_rows = 4 if is_small else 3
            self.query_one("#save-changes", PrimaryButton).styles.width = "100%" if is_small else 32

        except NoMatches:
            pass

    def on_resize(self) -> None:
        self.small = self.size.width <= 64

    @on(Button.Pressed, "#save-changes")
    async def save_changes(self) -> None:
        """Handles saving the changes made to personal information."""
        firstname = self.query_one("#first-name", TextInput).value
        lastname = self.query_one("#last-name", TextInput).value

        request = ProfileRequest(
            firstname=(firstname if firstname != "" else None),
            lastname=(lastname if lastname != "" else None),
        )

        result = await self.app.account.profile(request)

        if result.status != "success":
            self.notify(result.message, title="Profile", severity="error")
            return

        self.notify(result.message, title="Profile")

        self.user = result.user
        self.on_view_activated()

    def on_view_activated(self) -> None:
        if self.user is None:
            return

        self.query_one("#first-name", TextInput).value = self.user.firstname
        self.query_one("#last-name", TextInput).value = self.user.lastname
        self.query_one("#email", TextInput).value = self.user.email

    def on_view_closed(self) -> None:
        """Called when the view is closed."""
        pass
