from pathlib import Path
from typing import ClassVar

from textual.app import App
from textual.binding import Binding


class TUIApplication(App):
    """
    - Root application class
    """

    CSS_PATH = Path("styles") / Path("styles.tcss")
    TITLE = "Tennis App"
    SUB_TITLE = "Tennis App Local Client"

    BINDINGS: ClassVar[list] = [
        Binding("escape", "pop_screen", "Back"),
    ]

    def on_mount(self) -> None:
        """
        - Mounts first page
        """
        pass


if __name__ == "__main__":
    TUIApplication().run()
