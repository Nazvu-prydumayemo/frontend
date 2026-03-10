from textual.widgets import Input

class CustomInput(Input):
    """Кастомний інпут для тексту"""
    pass

class PasswordInput(Input):
    """Кастомний інпут для паролів"""
    def __init__(self, **kwargs):
        super().__init__(password=True, **kwargs)