"""Base class for all form widgets."""

from abc import abstractmethod
from typing import Any

from textual.app import ComposeResult
from textual.widget import Widget


class BaseForm(Widget):
    """Abstract base class for all form widgets in the application."""

    @abstractmethod
    def compose(self) -> ComposeResult:
        pass

    @abstractmethod
    def get_data(self) -> Any | str:
        """Retrieve and validate form data.

        Returns:
            A validated pydantic model on success, or a string error message on failure.
        """
        pass
