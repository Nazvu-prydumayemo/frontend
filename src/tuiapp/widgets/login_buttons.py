from textual.widgets import Button


class PrimaryButton(Button):
    """Primary action button."""

    def __init__(self, label: str, **kwargs):
        super().__init__(label, variant="primary", **kwargs)
        self.add_class("primary-button")


class SecondaryButton(Button):
    """Secondary action button."""

    def __init__(self, label: str, **kwargs):
        super().__init__(label, variant="default", **kwargs)
        self.add_class("secondary-button")
