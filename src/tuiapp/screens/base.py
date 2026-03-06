from textual.screen import Screen


class BaseScreen(Screen):
    """
    - Base Class for all screens
    - All screens should be derived from this
    """

    def change_screen(self, screen: str) -> None:
        """
        - Switches screen to given
        """

        self.app.push_screen(screen)

    def go_back(self) -> None:
        """
        - Switches to previous screen
        """
        self.app.pop_screen()
