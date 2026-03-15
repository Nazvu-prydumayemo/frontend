from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Button, Footer, Header, Static

from tuiapp.api.auth.schema import RegisterRequest, TokenResult
from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.forms.register_form import RegisterForm


class RegisterScreen(BaseScreen):
    """Register screen with register form."""

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
        response: TokenResult = await self.app.auth.register(json=data)

        self.toast(response.message)

        if response.status == "success" and response.token is not None:
            # TODO: Implement token handling
            return None
