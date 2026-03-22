"""Custom header widget with navigation buttons."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static

from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton


class Header(Widget):
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
                    yield SecondaryButton("Back", id="back-btn")

                yield PrimaryButton("Home", id="home-btn")
                yield PrimaryButton("Profile", id="profile-btn")
                yield SecondaryButton("Logout", id="logout-btn")

    @on(SecondaryButton.Pressed, "#back-btn")
    def action_back(self) -> None:
        """Go back to the previous screen."""
        self.screen.go_back()

    @on(PrimaryButton.Pressed, "#home-btn")
    def action_home(self) -> None:
        """Navigate to the hub screen."""
        self.screen.change_screen("hub")

    @on(PrimaryButton.Pressed, "#profile-btn")
    def action_profile(self) -> None:
        """Navigate to the profile screen."""
        self.screen.change_screen("profile")

    @on(SecondaryButton.Pressed, "#logout-btn")
    def action_logout(self) -> None:
        """Handle logout - shows WIP toast."""
        self.screen.toast("WIP")