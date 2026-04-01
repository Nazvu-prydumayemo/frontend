"""Login screen for user authentication."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button, Footer, Header, Static

from tuiapp.api.auth.schema import LoginRequest, TokenResult
from tuiapp.screens.base_screen import BaseScreen
from tuiapp.screens.hub_screen import HubScreen
from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.forms.login_form import LoginForm


class LoginScreen(BaseScreen):
    """Login screen with email and password form.

    Allows users to authenticate with their email and password credentials.
    On success, stores tokens and navigates to the hub screen.
    """

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
            self.notify(result, title="Login", severity="warning")
            return

        await self._login(result)

    @on(Button.Pressed, "#back")
    def back(self) -> None:
        self.go_back()

    async def _login(self, data: LoginRequest) -> None:
        button = self.query_one("#login", PrimaryButton)
        button.disabled = True

        response: TokenResult = await self.app.auth.login(json=data)

        if response.status != "success":
            self.notify(response.message, title="Login", severity="error")

        button.disabled = False

        if response.status == "success" and response.token is not None:
            self.app.token_manager.set_refresh_token(response.token.refresh_token)
            self.app.token_manager.access_token = response.token.access_token
            self.app.client.set_access_token(response.token.access_token)

            self.change_screen(HubScreen())
