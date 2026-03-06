from textual.widgets import Button


class PrimaryButton(Button):
    """Main action button (submit, login, confirm)."""

    DEFAULT_CLASSES = "btn-primary"


class SecondaryButton(Button):
    """Secondary action (cancel, back)."""

    DEFAULT_CLASSES = "btn-secondary"


class DangerButton(Button):
    """Dangerous actions (delete, logout)."""

    DEFAULT_CLASSES = "btn-danger"
