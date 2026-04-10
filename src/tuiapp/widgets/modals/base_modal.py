from abc import abstractmethod
from typing import ClassVar

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.events import Key
from textual.screen import ModalScreen


class BaseModal(ModalScreen[bool]):
    """Base class for all modals."""

    BINDINGS: ClassVar[list] = [
        Binding(key="ctrl+b", action="close", description="Close", tooltip="Close the modal")
    ]

    def action_close(self) -> None:
        self.dismiss(False)

    @on(Key)
    def on_key(self, event: Key) -> None:
        if event.key == "escape":
            event.stop()
            self.dismiss(False)

    def compose(self) -> ComposeResult:
        """Compose the modal with a centered container."""
        with Container(id="modal-container"):
            yield from self.compose_modal()

    """Each subclass should handle button events of the modal."""

    @abstractmethod
    def compose_modal(self) -> ComposeResult:
        """Each subclass should define the actual content of the modal."""
        pass
