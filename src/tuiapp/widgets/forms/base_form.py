from abc import abstractmethod
from typing import Any

from textual.app import ComposeResult
from textual.widget import Widget


class BaseForm(Widget):
    @abstractmethod
    def compose(self) -> ComposeResult:
        pass

    @abstractmethod
    def get_data(self) -> Any | str:
        pass
