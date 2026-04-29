from typing import ClassVar

from pydantic import EmailStr
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input, Static

from tuiapp.screens.base_screen import BaseScreen
from tuiapp.widgets.buttons import PrimaryButton
from tuiapp.widgets.forms.forgot_password_form import ForgotPasswordForm
from tuiapp.widgets.forms.new_password_form import NewPasswordForm
from tuiapp.widgets.inputs import CodeInput


class ForgotPasswordScreen(BaseScreen):
    sent_code: reactive[bool] = reactive(False)
    code: reactive[str | None] = reactive(None)
    email: EmailStr

    async def watch_sent_code(self, new_sent_code: bool | None) -> None:
        if new_sent_code is not None and new_sent_code:
            self.query_one(Vertical).remove()
            await self._mount_verify_code_section()

    async def watch_code(self, new_code: bool | None) -> None:
        if new_code is not None:
            self.query_one(Vertical).remove()
            await self._mount_new_password_section()

    BINDINGS: ClassVar[list] = [
        Binding(
            key="ctrl+b,escape",
            action="go_back",
            description="Back",
            tooltip="Go to the login screen",
        ),
    ]

    def action_go_back(self) -> None:
        self.app.switch_screen("login")

    def compose(self) -> ComposeResult:
        yield Header()
        yield from self._compose_email_section()
        yield Footer()

    def _compose_email_section(self) -> ComposeResult:
        with Vertical(classes="forgot-password-container"):
            yield Static("Input your email address and await a Password Reset Code", id="title")
            yield ForgotPasswordForm()
            yield PrimaryButton(
                "Send Reset Code", variant="primary", id="send-reset-code", classes="actions"
            )

    async def _mount_verify_code_section(self) -> None:
        new_container = Vertical(classes="forgot-password-container")
        await self.mount(new_container, before=self.query_one(Footer))

        await new_container.mount(Static("Enter the code sent to your email", id="title"))
        await new_container.mount(CodeInput(6))
        await new_container.mount(
            PrimaryButton("Continue", variant="primary", id="verify-code", classes="actions")
        )
        new_container.refresh(layout=True)

    async def _mount_new_password_section(self) -> None:
        new_container = Vertical(classes="forgot-password-container")
        await self.mount(new_container, before=self.query_one(Footer))

        await new_container.mount(Static("Create a new password", id="title"))
        await new_container.mount(NewPasswordForm())
        await new_container.mount(
            PrimaryButton(
                "Confirm New Password", variant="primary", id="set-new-password", classes="actions"
            )
        )
        new_container.refresh(layout=True)

    @on(Input.Submitted, "ForgotPasswordForm > .form-container > .field > #email")
    @on(Button.Pressed, "#send-reset-code")
    async def send_reset_code(self) -> None:
        data = self.query_one(ForgotPasswordForm).get_data()
        if isinstance(data, str):
            self.notify(data, title="Forgot Password", severity="error")
            return

        response = await self.app.auth.forgot_password(data)
        if response.status != "success":
            self.notify(response.message, title="Forgot Password", severity="error")
            return

        self.notify(response.message, title="Forgot Password", severity="information")
        self.email = data.email
        self.sent_code = True

    @on(Button.Pressed, "#verify-code")
    def verify_code(self) -> None:
        code = self.query_one(CodeInput).get_data()
        if not code:
            self.notify("Please input your code")
            return

        self.notify(f"Your code is {code}")
        self.code = code
        # TODO: Add logic here

    @on(Input.Submitted, "NewPasswordForm > .form-container > #confirm-field > #confirm")
    @on(Button.Pressed, "#set-new-password")
    def set_new_password(self) -> None:
        password_data = self.query_one(NewPasswordForm).get_data()
        if isinstance(password_data, str):
            self.notify(password_data)
            return

        # TODO: Add logic here
        self.app.switch_screen("login")
