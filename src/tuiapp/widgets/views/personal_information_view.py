from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button

from tuiapp.widgets.buttons import PrimaryButton, SecondaryButton
from tuiapp.widgets.inputs import TextInput
from tuiapp.widgets.views.base_view import BaseView

class PersonalInformationView(BaseView):
    """Вид профілю для перегляду та редагування особистої інформації."""

    def compose_view(self) -> ComposeResult:
        with Vertical(classes="personal-info-view"):
            yield Static("Особиста інформація", classes="view-title")
            
            with Horizontal(classes="name-row"):
                with Vertical(classes="field-group"):
                    yield Static("Ім'я", classes="field-label")
                    yield TextInput(placeholder="Введіть ім'я", id="first-name")
                with Vertical(classes="field-group"):
                    yield Static("Прізвище", classes="field-label")
                    yield TextInput(placeholder="Введіть прізвище", id="last-name")

            with Vertical(classes="field-group"):
                yield Static("Електронна пошта", classes="field-label")
                yield TextInput(placeholder="email@example.com", id="email", disabled=True)

            with Horizontal(classes="actions-row"):
                yield PrimaryButton("Зберегти", id="save-changes")
                yield SecondaryButton("Скасувати", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Використовуємо notify, оскільки toast у BaseScreen може конфліктувати з шарами
        self.app.notify(f"Виконано: {event.button.id}")

    def on_view_activated(self) -> None: pass
    def on_view_closed(self) -> None: pass