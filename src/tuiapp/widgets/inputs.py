from textual.widgets import Input


class TextInput(Input):
    """Text input component."""

    def __init__(self, placeholder: str, **kwargs):
        super().__init__(placeholder=placeholder, **kwargs)
        self.add_class("text-input")


class PasswordInput(Input):
    """Password input component."""

    def __init__(self, placeholder: str = "Password", **kwargs):
        super().__init__(password=True, placeholder=placeholder, **kwargs)
        self.add_class("text-input")
