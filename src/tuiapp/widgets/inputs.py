from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, Input


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
            )
            yield Button(self.SHOW, id="toggle-password", classes="toggle-btn")

    def on_button_pressed(self, event: Button.Pressed):
        field = self.query_one("#password-field", Input)
        field.password = not field.password
        event.button.label = self.SHOW if field.password else self.HIDE

    @property
    def value(self):
        return self.query_one("#password-field", Input).value
