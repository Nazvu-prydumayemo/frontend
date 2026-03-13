from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button, Footer, Header, Static

from tuiapp.api.auth.schema import LoginRequest, Token
from tuiapp.api.errors import APIError
from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.forms.login_form import LoginForm


class LoginScreen(BaseScreen):
    """Login screen with email and password form."""

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(id="login-container"):
                yield Static("LOGIN", id="login-title")
                yield LoginForm()
                yield PrimaryButton("Login", id="login")
                yield SecondaryButton("Back", id="back")
        yield Footer()

    @on(Button.Pressed, "#login")
    async def login(self) -> None:
        data = self.query_one(LoginForm).get_data()

        if data is None:
            self.toast("All fields required!")
            return

        await self._login(data)

    @on(Button.Pressed, "#back")
    def back(self) -> None:
        self.go_back()

    async def _login(self, data: LoginRequest) -> None:
        try:
            token: Token | None = await self.app.auth.login(json=data)

        except APIError as e:
            if e.status_code == 0:
                self.toast("Network error, please try again!")

            else:
                self.toast(f"Something went wrong! ({e.status_code})")

            return

        if token is None:
            self.toast("Incorrect credentials!")
            return

        self.toast("Successful Login!")
        # TODO: Manage Tokens
