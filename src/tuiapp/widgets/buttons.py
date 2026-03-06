from textual.widgets import Button


class PrimaryButton(Button):
    """
    - Used for main actions (submit, login, confirm)
    """

    DEFAULT_CLASSES = "btn-primary"


class SecondaryButton(Button):
    """
    - Used for secondary actions (cancel, back)
    """

    DEFAULT_CLASSES = "btn-secondary"


class DangerButton(Button):
    """
    - Used for dangerous actions (delete, logout)
    """

    DEFAULT_CLASSES = "btn-danger"
