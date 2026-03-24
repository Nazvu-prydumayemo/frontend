"""Registration screen for creating new user accounts."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button, Footer, Header, Static

from tuiapp.api.auth.schema import RegisterRequest, TokenResult
from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.forms.register_form import RegisterForm


class RegisterScreen(BaseScreen):
    """Registration screen for creating new user accounts.

    Collects user details and registers a new account with the backend.
    On success, stores tokens and navigates to the hub screen.
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(id="register-container"):
                yield Static("REGISTER", id="register-title")
                yield RegisterForm()
                yield PrimaryButton("Register", id="register")
                yield SecondaryButton("Back", id="back")
        yield Footer()

    @on(Button.Pressed, "#register")
    async def register(self) -> None:
        result = self.query_one(RegisterForm).get_data()

        if isinstance(result, str):
            self.toast(result)
            return

        await self._register(result)

    @on(Button.Pressed, "#back")
    def back(self) -> None:
        self.go_back()

    async def _register(self, data: RegisterRequest) -> None:
        button = self.query_one("#register", PrimaryButton)
        button.disabled = True

        response: TokenResult = await self.app.auth.register(json=data)

        self.toast(response.message)
        button.disabled = False

        if response.status == "success" and response.token is not None:
            self.app.token_manager.set_refresh_token(response.token.refresh_token)
            self.app.token_manager.access_token = response.token.access_token
            self.app.client.set_access_token(response.token.access_token)

            self.change_screen("hub")