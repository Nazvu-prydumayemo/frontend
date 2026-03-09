from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Vertical, Center

from widgets.login_form import LoginFormComponent


LOGIN_CSS = """
Screen {
    background: white;
    align: center middle;
}

#screen-container {
    width: 50;
    height: auto;
    align: center middle;
}

#title {
    text-align: center;
    text-style: bold;
    color: black;
    margin-bottom: 1;
    padding: 1 0;
    height: 5;
}

#form-container {
    width: 100%;
    height: auto;
    padding: 0 1;
}

.field-label {
    color: black;
    margin-top: 1;
    margin-bottom: 0;
}

.text-input {
    border: solid black;
    background: white;
    color: black;
    width: 100%;
    margin-bottom: 0;
    height: 3;
}

.text-input:focus {
    border: solid $primary;
}

.primary-button {
    width: 100%;
    background: $primary;
    color: white;
    margin-top: 1;
    margin-bottom: 1;
    border: none;
    height: 3;
}

.secondary-button {
    width: 100%;
    background: #eeeeee;
    color: #666666;
    border: none;
    height: 3;
}
"""


class LoginScreen(App):
    """Login Screen application."""

    CSS = LOGIN_CSS

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="screen-container"):
                yield Static("LOGIN", id="title")
                yield LoginFormComponent()

    def on_button_pressed(self, event) -> None:
        button_id = event.button.id

        if button_id == "login":
            email = self.query_one("#email").value
            password = self.query_one("#password").value
            # Handle login logic here
            self.notify(f"Logging in as: {email}")

        elif button_id == "back":
            self.notify("Going back...")
            self.exit()


if __name__ == "__main__":
    app = LoginScreen()
    app.run()