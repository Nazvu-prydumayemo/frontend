"""Login screen for user authentication."""

from typing import ClassVar

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Input, Static

from tuiapp.api.auth.schema import LoginRequest, TokenResult
from tuiapp.screens.base_screen import BaseScreen
from tuiapp.screens.forgot_password_screen import ForgotPasswordScreen
from tuiapp.screens.hub_screen import HubScreen
from tuiapp.widgets.buttons import PrimaryButton
from tuiapp.widgets.forms.login_form import LoginForm


class LoginScreen(BaseScreen):
    """Login screen with email and password form.

    Allows users to authenticate with their email and password credentials.
    On success, stores tokens and navigates to the hub screen.
    """

    BINDINGS: ClassVar[list] = [
        Binding(
            key="ctrl+b,escape",
            action="go_back",
            description="Back",
            tooltip="Go to the main screen",
        ),
        Binding(
            key="ctrl+r",
            action="go_signup",
            description="Signup",
            tooltip="Go to the signup screen",
        ),
    ]

    def action_go_back(self) -> None:
        self.app.switch_screen("main")

    def action_go_signup(self) -> None:
        self.app.switch_screen("register")

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="login-container"):
            yield Static(
                r"""
▄▄    ▄▄▄   ▄▄▄▄ ▄▄ ▄▄  ▄▄
██   ██▀██ ██ ▄▄ ██ ███▄██
████ ▀███▀ ▀███▀ ██ ██ ▀██
""",
                id="title",
            )
            yield LoginForm()
            yield PrimaryButton("Login", variant="primary", id="login")
            yield PrimaryButton("Forgot Password?", id="forgot-password")
        yield Footer()

    @on(Button.Pressed, "#forgot-password")
    def forgot_password(self) -> None:
        self.app.switch_screen(ForgotPasswordScreen())

    @on(Input.Submitted, "#password-field")
    @on(Button.Pressed, "#login")
    async def login(self) -> None:
        result = self.query_one(LoginForm).get_data()

        if isinstance(result, str):
            self.notify(result, title="Login", severity="warning")
            return

        await self._login(result)

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

            self.app.switch_screen(HubScreen())
