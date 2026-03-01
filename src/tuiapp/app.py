from textual.app import App
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button


class TUIApplication(App[Screen]):
    """Minimal Textual App skeleton for mypy"""

    def compose(self):
        """Define the UI layout."""
        yield Vertical(
            Button("Login"),
            Button("Register"),
        )


if __name__ == "__main__":
    TUIApplication().run()
