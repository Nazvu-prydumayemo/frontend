import re

from textual.containers import Horizontal
from textual.validation import ValidationResult, Validator
from textual.widget import Widget
from textual.widgets import Button, Input, MaskedInput


class PasswordValidator(Validator):
    RE_MIN_LENGTH = r".{8,}"
    RE_LOWERCASE = r"[a-z]"
    RE_UPPERCASE = r"[A-Z]"
    RE_DIGIT = r"\d"
    RE_SPECIAL = r"[^A-Za-z0-9]"

    def validate(self, value: str) -> ValidationResult:
        if not re.search(self.RE_MIN_LENGTH, value):
            return self.failure("At least 8 characters")

        if not re.search(self.RE_UPPERCASE, value):
            return self.failure("At least one uppercase letter")

        if not re.search(self.RE_LOWERCASE, value):
            return self.failure("At least one lowercase letter")

        if not re.search(self.RE_DIGIT, value):
            return self.failure("At least one number")

        if not re.search(self.RE_SPECIAL, value):
            return self.failure("At least one special character")

        return self.success()


class DigitInput(MaskedInput):
    def __init__(self, **kwargs):
        super().__init__(template="9", placeholder="0", **kwargs)
        self.add_class("digit-input")


class TextInput(Input):
    """Text input component."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_class("text-input")


class PasswordInput(Widget):
    """Password input component with show/hide toggle."""

    SHOW = "S"
    HIDE = "H"

    def __init__(self, placeholder: str = "Password", **kwargs):
        super().__init__(**kwargs)
        self._placeholder = placeholder

    def compose(self):
        with Horizontal(classes="password-row"):
            yield Input(
                password=True,
                placeholder=self._placeholder,
                id="password-field",
                classes="text-input",
                validators=(PasswordValidator()),
            )
            yield Button(self.SHOW, id="toggle-password", classes="toggle-btn")

    def on_button_pressed(self, event: Button.Pressed):
        field = self.query_one("#password-field", Input)
        field.password = not field.password
        event.button.label = self.SHOW if field.password else self.HIDE

    @property
    def value(self):
        return self.query_one("#password-field", Input).value

    @property
    def is_valid(self) -> bool:
        field = self.query_one("#password-field", Input)
        return field.is_valid
