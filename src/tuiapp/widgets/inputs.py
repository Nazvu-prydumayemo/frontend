import re

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.events import Key
from textual.reactive import reactive
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


class CodeInput(Widget):
    is_complete: reactive[bool] = reactive(False)

    def __init__(self, length: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.length = length
        self.add_class("code-input")

    def compose(self) -> ComposeResult:
        with Horizontal():
            for i in range(self.length):
                yield DigitInput(id=f"digit-{i}")

    def on_mount(self) -> None:
        self.query(DigitInput).first().focus()

    def _get_digit(self, index: int) -> DigitInput | None:
        return self.query_one(f"#digit-{index}", DigitInput)

    def _focus_next(self, current_index: int) -> None:
        if current_index < self.length - 1:
            self._get_digit(current_index + 1).focus()  # type: ignore

    def _focus_prev(self, current_index: int) -> None:
        if current_index > 0:
            self._get_digit(current_index - 1).focus()  # type: ignore

    @on(MaskedInput.Changed)
    def on_digit_changed(self, event: MaskedInput.Changed) -> None:
        event.stop()
        index = int(event.input.id.split("-")[1])  # type: ignore

        if event.value:
            event.input.add_class("-filled")
            self._focus_next(index)
        else:
            event.input.remove_class("-filled")

        self.is_complete = self._check_complete()

    def on_key(self, event: Key) -> None:
        focused = self.app.focused
        if not isinstance(focused, DigitInput):
            return

        index = int(focused.id.split("-")[1])  # type: ignore

        if event.key == "backspace":
            event.stop()
            if focused.value:
                focused.value = ""
            else:
                self._focus_prev(index)

        elif event.key == "left":
            event.stop()
            self._focus_prev(index)

        elif event.key == "right":
            event.stop()
            self._focus_next(index)

    def _check_complete(self) -> bool:
        return all(inp.value for inp in self.query(DigitInput))

    def get_data(self) -> str | None:
        inputs = self.query(DigitInput)
        if not all(inp.value for inp in inputs):
            return None
        return "".join(inp.value for inp in inputs)

    def clear(self) -> None:
        for inp in self.query(DigitInput):
            inp.value = ""
            inp.remove_class("-filled")

        self.query(DigitInput).first().focus()
        self.is_complete = False


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
