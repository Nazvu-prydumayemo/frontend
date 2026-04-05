"""Registration screen for creating new user accounts."""

from typing import ClassVar

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input, Static

from tuiapp.api.auth.schema import RegisterRequest, TokenResult
from tuiapp.screens.base_screen import BaseScreen
from tuiapp.screens.hub_screen import HubScreen
from tuiapp.widgets.buttons import PrimaryButton
from tuiapp.widgets.forms.register_form import RegisterForm
from tuiapp.widgets.modals.password_hints_modal import PasswordHintsModal


class RegisterScreen(BaseScreen):
    """Registration screen for creating new user accounts.

    Collects user details and registers a new account with the backend.
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
            action="go_login",
            description="Login",
            tooltip="Go to the login screen",
        ),
        Binding(
            key="ctrl+g",
            action="push_hints",
            description="Password Requirements",
            tooltip="Password Requirements",
        ),
    ]

    def action_go_back(self) -> None:
        self.app.switch_screen("main")

    def action_go_login(self) -> None:
        self.app.switch_screen("login")

    def action_push_hints(self) -> None:
        self.show_modal(PasswordHintsModal())

    small: reactive[bool] = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="register-container"):
            yield Static(
                r"""
▄█████ ██  ▄████  ███  ██ ██  ██ █████▄
▀▀▀▄▄▄ ██ ██  ▄▄▄ ██ ▀▄██ ██  ██ ██▄▄█▀
█████▀ ██  ▀███▀  ██   ██ ▀████▀ ██    
""",
                id="title",
            )
            yield RegisterForm()
            yield PrimaryButton("Signup", id="register")
        yield Footer()

    def watch_small(self, is_small: bool) -> None:
        try:
            self.query_one("#title", Static).display = not is_small
            form = self.query_one("#register-form", Container)
            form.styles.grid_size_columns = 1 if is_small else 2
            form.styles.grid_size_rows = 5 if is_small else 3
            self.query_one("#register", PrimaryButton).styles.width = 32 if is_small else 56

        except NoMatches:
            pass

    def on_resize(self) -> None:
        self.small = self.size.width <= 64

    @on(Input.Submitted, "#confirm > .password-row > #password-field")
    @on(Button.Pressed, "#register")
    async def register(self) -> None:
        result = self.query_one(RegisterForm).get_data()

        if isinstance(result, str):
            self.notify(result, title="Signup", severity="warning")
            return

        await self._register(result)

    async def _register(self, data: RegisterRequest) -> None:
        button = self.query_one("#register", PrimaryButton)
        button.disabled = True

        response: TokenResult = await self.app.auth.register(json=data)

        if response.status != "success":
            self.notify(response.message, title="Signup", severity="error")

        button.disabled = False

        if response.status == "success" and response.token is not None:
            self.app.token_manager.set_refresh_token(response.token.refresh_token)
            self.app.token_manager.access_token = response.token.access_token
            self.app.client.set_access_token(response.token.access_token)

            self.app.switch_screen(HubScreen())
