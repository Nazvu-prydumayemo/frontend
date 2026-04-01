from abc import abstractmethod

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen


class BaseModal(ModalScreen):
    """Base class for all modals."""

    def compose(self) -> ComposeResult:
        """Compose the modal with a centered container."""
        with Container(id="modal-container"):
            yield from self.compose_modal()

    """Each subclass should handle button events of the modal."""

    @abstractmethod
    def compose_modal(self) -> ComposeResult:
        """Each subclass should define the actual content of the modal."""
        pass
