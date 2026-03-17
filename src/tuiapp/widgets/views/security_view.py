from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Button

from tuiapp.widgets.buttons import PrimaryButton, DangerButton
from tuiapp.widgets.inputs import PasswordInput
from tuiapp.widgets.modals.delete_account_modal import DeleteAccountModal
from tuiapp.widgets.views.base_view import BaseView

class SecurityView(BaseView):
    """Вид профілю для налаштувань безпеки."""

    def compose_view(self) -> ComposeResult:
        with Vertical(classes="security-view"):
            yield Static("Зміна пароля", classes="view-title")
            
            yield Vertical(Static("Новий пароль", classes="field-label"), 
                          PasswordInput(placeholder="Введіть пароль", id="sec-new-password"))
            
            yield PrimaryButton("Оновити", id="update-password")

            with Vertical(classes="delete-account-section"):
                yield Static("Видалення акаунта", classes="view-title-danger")
                yield DangerButton("Видалити мій профіль", id="open-delete-modal")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "open-delete-modal":
            # Викликаємо модальне вікно безпосередньо через додаток
            self.app.push_screen(DeleteAccountModal())
        else:
            self.app.notify(f"Дія {event.button.id} ще в розробці")

    def on_view_activated(self) -> None: pass
    def on_view_closed(self) -> None: pass