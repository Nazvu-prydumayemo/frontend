from abc import abstractmethod

from textual.app import ComposeResult
from textual.containers import Container

from tuiapp.screens.base_screen import BaseScreen


class BaseView(Container):
    """Base class for all views."""

    DEFAULT_CLASSES = "view-container"

    def compose(self) -> ComposeResult:
        yield from self.compose_view()

    """Each subclass should handle button events of the view."""

    @abstractmethod
    def compose_view(self) -> ComposeResult:
        """Each subclass should define the actual content of the view."""
        pass

    @abstractmethod
    def on_view_activated(self) -> None:
        """Each subclass should define what happens when the view is activated."""
        pass

    @abstractmethod
    def on_view_closed(self) -> None:
        """Each subclass should define what happens the view is closed."""
        pass

    @property
    def screen(self) -> BaseScreen:
        return super().screen  # type: ignore
