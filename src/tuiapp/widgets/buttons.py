from textual.widgets import Button


class PrimaryButton(Button):
    """Button for primary actions such as submit, login, or confirm."""

    DEFAULT_CLASSES = "btn-primary"


class SecondaryButton(Button):
    """Button for secondary actions such as cancel or back."""

    DEFAULT_CLASSES = "btn-secondary"


class DangerButton(Button):
    """Button for dangerous actions such as delete or logout."""

    DEFAULT_CLASSES = "btn-danger"
