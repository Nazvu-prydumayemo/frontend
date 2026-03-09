from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static
from textual.containers import Vertical, Horizontal


class RegisterApp(App):

    CSS = """
    Screen {
        align: center middle;
        background: #1e1e1e;
    }

    #card {
        width: 58;
        padding: 2 4;
        background: white;
        border: round #cfcfcf;
    }

    #title {
        width: 100%;
        content-align: center middle;
        color: black;
        text-style: bold;
        margin-bottom: 1;
    }

    .label {
        color: black;
        margin-top: 1;
        margin-bottom: 0;
    }

    Input {
        width: 100%;
        margin-bottom: 1;
        color: black;
        background: white;
        border: solid #bbbbbb;
    }

    .password_row {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }

    .password_row Input {
        width: 1fr;
        margin-right: 1;
    }

    .toggle_btn {
        width: 6;
        background: #f3f4f6;
        color: black;
        border: solid #bbbbbb;
    }

    #register_btn {
        width: 100%;
        background: #2563eb;
        color: white;
        text-style: bold;
        margin-top: 1;
        margin-bottom: 1;
    }

    #back_btn {
        width: 100%;
        background: #e5e7eb;
        color: black;
        border: solid #bbbbbb;
    }
    """

    def compose(self) -> ComposeResult:
        yield Vertical(

            Static("Registration", id="title"),

            Static("Name - Lastname", classes="label"),
            Input(placeholder="Your Name-Lastname", id="name"),

            Static("Email", classes="label"),
            Input(placeholder="Your Email", id="email"),

            Static("Password", classes="label"),
            Horizontal(
                Input(password=True, placeholder="Password", id="password"),
                Button("👁", id="toggle_password", classes="toggle_btn"),
                classes="password_row",
            ),

            Static("Confirm Password", classes="label"),
            Horizontal(
                Input(password=True, placeholder="Confirm Password", id="confirm"),
                Button("👁", id="toggle_confirm", classes="toggle_btn"),
                classes="password_row",
            ),

            Button("Register", id="register_btn"),
            Button("Back", id="back_btn"),

            id="card",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "toggle_password":
            field = self.query_one("#password", Input)
            field.password = not field.password

        elif event.button.id == "toggle_confirm":
            field = self.query_one("#confirm", Input)
            field.password = not field.password

        elif event.button.id == "register_btn":

            name = self.query_one("#name", Input).value
            email = self.query_one("#email", Input).value
            password = self.query_one("#password", Input).value
            confirm = self.query_one("#confirm", Input).value

            if not name or not email or not password or not confirm:
                self.notify("Fill in all fields")
                return

            if password != confirm:
                self.notify("Passwords do not match")
                return

            self.notify("Registration successful")

        elif event.button.id == "back_btn":
            self.exit()


if __name__ == "__main__":
    RegisterApp().run()