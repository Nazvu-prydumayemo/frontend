from textual.app import RenderResult
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static

from tuiapp.api.court.schema import CourtScheduleSlot


class ScheduleSlot(Static):
    """A pressable button representing a single bookable time slot."""

    DEFAULT_CSS = ""

    pressed: reactive[bool] = reactive(False)

    def __init__(self, slot: CourtScheduleSlot, **kwargs) -> None:
        super().__init__("", **kwargs)
        self.slot = slot

    def render(self) -> RenderResult:
        start = self.slot.start_time.strftime("%H:%M")
        return f"{start}"

    def on_mount(self) -> None:
        self._sync_classes()

    def _sync_classes(self) -> None:
        self.set_class(not self.slot.is_available, "-unavailable")
        self.set_class(self.pressed, "-pressed")

    def on_click(self) -> None:
        if not self.slot.is_available:
            return

        self.pressed = not self.pressed
        self._sync_classes()

        if self.pressed:
            self.post_message(ScheduleSlot.Selected(self, self.slot.id))
        else:
            self.post_message(ScheduleSlot.Deselected(self, self.slot.id))

    class Selected(Message):
        """Posted when the slot is selected."""

        def __init__(self, button: "ScheduleSlot", slot_id: int) -> None:
            super().__init__()
            self.button = button
            self.slot_id = slot_id

    class Deselected(Message):
        """Posted when the slot is deselected."""

        def __init__(self, button: "ScheduleSlot", slot_id: int) -> None:
            super().__init__()
            self.button = button
            self.slot_id = slot_id
