from typing import TYPE_CHECKING, cast

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton

if TYPE_CHECKING:
    from tuiapp.screens.base_screen import BaseScreen


class TUIHeader(Widget):
    """Custom header widget with navigation buttons.

    The header displays:
    - App name on the left
    - Navigation buttons on the right (Back, Home, Profile, Logout)

    The Back button is shown conditionally based on the current screen.
    """

    def __init__(self, screen_name: str = "hub", **kwargs):
        """Initialize the header.

        Args:
            screen_name: Name of the current screen (e.g., "hub", "profile")
            **kwargs: Additional keyword arguments passed to Widget
        """
        super().__init__(**kwargs)
        self.screen_name = screen_name.lower()

    def compose(self) -> ComposeResult:
        """Compose the header with app name and navigation buttons."""
        with Horizontal():
            yield Static("NP-Tennis", id="app-name")
            yield Static("", classes="spacer")

            with Horizontal(id="nav-buttons"):
                if self.screen_name != "hub":
                    yield SecondaryButton("Back", id="back-btn", flat=True)

                yield PrimaryButton("Home", id="home-btn", flat=True)
                yield PrimaryButton("Profile", id="profile-btn", flat=True)
                yield SecondaryButton("Logout", id="logout-btn", flat=True)

    @on(SecondaryButton.Pressed, "#back-btn")
    def action_back(self) -> None:
        cast("BaseScreen", self.screen).go_back()

    @on(PrimaryButton.Pressed, "#home-btn")
    def action_home(self) -> None:
        if self.screen_name != "hub":
            from tuiapp.screens.hub_screen import HubScreen

            cast("BaseScreen", self.screen).app.switch_screen(HubScreen())

    @on(PrimaryButton.Pressed, "#profile-btn")
    def action_profile(self) -> None:
        if self.screen_name != "profile":
            from tuiapp.screens.profile_screen import ProfileScreen

            cast("BaseScreen", self.screen).app.switch_screen(ProfileScreen())

    @on(SecondaryButton.Pressed, "#logout-btn")
    def action_logout(self) -> None:
        cast("BaseScreen", self.screen).app.token_manager.logout()
        cast("BaseScreen", self.screen).notify("Goodbye!", title="Logout")
