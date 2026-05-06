"""Court cards vertical scrollable container widget."""

from textual.containers import VerticalScroll


class CardContainer(VerticalScroll):
    """A scrollable vertical container for CourtCard widgets.

    Docked to the left side of the screen, houses multiple CourtCard widgets.
    """

    DEFAULT_CLASSES = "card-container"
