from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from textual.binding import Binding
from textual.screen import Screen

from tuiapp.api.auth.auth_guard import AuthGuard
from tuiapp.widgets.modals.confirmation_modal import ConfirmationModal

if TYPE_CHECKING:
    from textual.types import CallbackType

    from tuiapp.app import TUIApplication
    from tuiapp.widgets.modals.base_modal import BaseModal


class BaseScreen(Screen):
    """Base screen class. All screens should inherit from this."""

    if TYPE_CHECKING:
        app: TUIApplication  # type: ignore

    def show_modal(self, modal: BaseModal, callback: CallbackType | Any | None = None) -> None:
        """Shows a modal by pushing it onto the stack.

        Args:
            modal: The modal to show.
        """
        self.app.push_screen(modal, callback)  # type: ignore

    def go_back(self) -> None:
        """Return to the previous screen by popping the current screen."""
        self.app.pop_screen()


class AuthScreen(AuthGuard, BaseScreen):  # type: ignore
    BINDINGS: ClassVar[list[Binding]] = [
        Binding(
            key="ctrl+l",
            action="logout",
            description="Logout",
            tooltip="Logout",
        ),
        Binding(
            key="ctrl+r",
            action="go_hub",
            description="Hub",
            tooltip="Go to the hub page",
        ),
        Binding(
            key="ctrl+u",
            action="go_profile",
            description="Profile",
            tooltip="Go to the profile page",
        ),
    ]

    def _check_logout(self, logout: bool | None) -> None:
        if logout:
            self.app.token_manager.logout()
            self.notify("Goodbye!", title="Logout")

    def action_logout(self) -> None:
        self.show_modal(ConfirmationModal("Logout"), self._check_logout)

    def action_go_hub(self) -> None:
        from tuiapp.screens.hub_screen import HubScreen

        self.app.switch_screen(HubScreen())

    def action_go_profile(self) -> None:
        from tuiapp.screens.profile_screen import ProfileScreen

        self.app.switch_screen(ProfileScreen())
