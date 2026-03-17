from abc import abstractmethod

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen

from tuiapp.widgets.toast import Toast


class BaseModal(ModalScreen):
    """Base class for all modals."""

    def compose(self) -> ComposeResult:
        """Compose the modal with a centered container."""
        with Container(id="modal-container"):
            yield from self.compose_modal()

    """Each subclass should handle button events of the modal."""

    def toast(self, message: str, duration: float = 3.0) -> None:
        """Display a toast notification popup.

        Args:
            message: The message to display in the toast.
            duration: How long to display the toast in seconds.
        """
        self.mount(Toast(message, duration))

    @abstractmethod
    def compose_modal(self) -> ComposeResult:
        """Each subclass should define the actual content of the modal."""
        pass
