from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, Static


class Header(Widget):
    """Custom header widget with navigation buttons.
    
    The header displays:
    - App name on the left
    - Navigation buttons on the right (Back, Home, Profile, Logout)
    
    Buttons are shown/hidden based on the current screen.
    """

    DEFAULT_CSS = """
    Header {
        dock: top;
        height: 3;
        background: $panel;
        border-bottom: solid $primary;
    }
    
    Header > Horizontal {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    Header #app-name {
    width: auto;
    margin-left: 2;
    padding-top: 1;
    text-style: bold;
    }
    
    Header .spacer {
        width: 1fr;
    }
    
    Header #nav-buttons {
        width: auto;
        margin-right: 2;
    }
    
    Header Button {
        margin: 0 1;
        min-width: 8;
    }
    
    Header Button:first-child {
        margin-left: 0;
    }
    
    Header Button:last-child {
        margin-right: 0;
    }
    """

    def __init__(self, screen_name: str = "main", **kwargs):
        """Initialize the header.
        
        Args:
            screen_name: Name of the current screen (e.g., "main", "hub", "profile", "login")
            **kwargs: Additional keyword arguments passed to Widget
        """
        super().__init__(**kwargs)
        self.screen_name = screen_name.lower()

    def compose(self) -> ComposeResult:
        """Compose the header with app name and navigation buttons."""
        with Horizontal():
            # App name on the left
            yield Static("NP-Tennis", id="app-name")
            
            # Spacer to push buttons to the right
            yield Static("", classes="spacer")
            
            # Navigation buttons on the right
            with Horizontal(id="nav-buttons"):
                # Back button - show if not at hub or main
                if self.screen_name not in ["hub", "main"]:
                    yield Button("Back", id="back-btn", variant="default")
                
                # Home button - show if not at hub or main
                if self.screen_name not in ["hub", "main"]:
                    yield Button("Home", id="home-btn", variant="default")
                
                # Profile button - show if not at profile
                if self.screen_name != "profile":
                    yield Button("Profile", id="profile-btn", variant="default")
                
                # Logout button - always show
                yield Button("Logout", id="logout-btn", variant="default")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        event.stop()
        
        button_id = event.button.id
        
        if button_id == "back-btn":
            self.handle_back()
        elif button_id == "home-btn":
            self.handle_home()
        elif button_id == "profile-btn":
            self.handle_profile()
        elif button_id == "logout-btn":
            self.handle_logout()

    def handle_back(self) -> None:
        """Go back to the previous screen if not at hub or main."""
        if self.screen_name not in ["hub", "main"]:
            self.screen.go_back()

    def handle_home(self) -> None:
        """Navigate to the hub screen if not at hub."""
        if self.screen_name != "hub":
            self.screen.change_screen("hub")

    def handle_profile(self) -> None:
        """Navigate to the profile screen if not at profile."""
        if self.screen_name != "profile":
            self.screen.change_screen("profile")

    def handle_logout(self) -> None:
        """Handle logout - shows WIP toast."""
        self.screen.toast("WIP")