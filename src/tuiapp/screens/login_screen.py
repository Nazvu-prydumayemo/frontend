from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button, Footer, Header, Static

from tuiapp.api.auth.schema import LoginRequest, LoginResult
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
        result = self.query_one(LoginForm).get_data()

        if isinstance(result, str):
            self.toast(result)
            return

        await self._login(result)

    @on(Button.Pressed, "#back")
    def back(self) -> None:
        self.go_back()

    async def _login(self, data: LoginRequest) -> None:
        response: LoginResult = await self.app.auth.login(json=data)

        self.toast(response.message)

        if response.status == "success" and response.token is not None:
            # TODO: Implement token handling
            return None
