from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button

from tuiapp.widgets.buttons import SecondaryButton, DangerButton
from tuiapp.widgets.inputs import PasswordInput
from tuiapp.widgets.modals.base_modal import BaseModal

class DeleteAccountModal(BaseModal):
    """Модальне вікно для підтвердження видалення."""

    def compose_modal(self) -> ComposeResult:
        # Важливо: використовуємо id="modal-container" для роботи вашого CSS
        with Vertical(id="modal-container"):
            yield Static("Ви впевнені?", id="modal-status-message")
            yield Static("Ця дія є незворотною. Введіть пароль:", classes="modal-subtext")
            
            # Встановлюємо унікальний ID саме для віджета PasswordInput
            yield PasswordInput(placeholder="Пароль підтвердження", id="modal-confirm-pass")
            
            with Horizontal(classes="modal-buttons"):
                yield SecondaryButton("Скасувати", id="modal-cancel")
                yield DangerButton("Видалити", id="modal-confirm-action")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "modal-cancel":
            self.dismiss()
        
        elif event.button.id == "modal-confirm-action":
            # Отримуємо PasswordInput за ID
            confirm_widget = self.query_one("#modal-confirm-pass", PasswordInput)
            # Беремо значення через property .value (яке ви прописали в inputs.py)
            password = confirm_widget.value
            
            if not password:
                self.app.notify("Будь ласка, введіть пароль", severity="error")
                return
            
            self.app.notify("Профіль видалено (симуляція)", severity="warning")
            self.dismiss(True)