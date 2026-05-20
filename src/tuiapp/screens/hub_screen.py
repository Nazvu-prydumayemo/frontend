"""Hub screen - the main authenticated user dashboard."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.css.query import NoMatches
from textual.events import Mount
from textual.reactive import reactive
from textual.widgets import Footer, Header

from tuiapp.api.court.schema import Court
from tuiapp.screens.base_screen import AuthScreen
from tuiapp.widgets.courts.card_container import CardContainer
from tuiapp.widgets.courts.court_card import CourtCard
from tuiapp.widgets.views.court_view import CourtView


class HubScreen(AuthScreen):
    """Main dashboard screen displayed after successful authentication."""

    courts: reactive[list[Court] | None] = reactive(None)
    selected_court: reactive[Court | None] = reactive(None)

    PAGE_SIZE = 100

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.page = 0

    def _get_page_offset(self, page: int) -> int:
        return page * self.PAGE_SIZE

    @on(Mount)
    async def _auth_guard(self) -> None:
        await super()._auth_guard()
        await self._load_courts()

    async def _load_courts(self) -> None:
        result = await self.app.court.get_all_courts(
            self._get_page_offset(self.page), self.PAGE_SIZE
        )
        if result.status != "success":
            self.notify(result.message, title="Courts", severity="error")
            return

        self.courts = result.courts.items if result.courts and result.courts.items else None
        self.selected_court = self.courts[0] if self.courts else None
        self.page += 1

    def watch_selected_court(self, new_court: Court | None = None) -> None:
        try:
            for card in self.query(CourtCard):
                card.selected = card.court == new_court

            view = self.query_one(CourtView)
            view.court = new_court
        except NoMatches:
            pass

    def watch_courts(self, new_courts: list[Court] | None = None) -> None:
        try:
            container = self.query_one(CardContainer)
            container.remove_children()

            if not new_courts:
                return

            for court in new_courts:
                card = CourtCard(court=court)
                card.selected = court == self.selected_court
                container.mount(card)

        except NoMatches:
            pass

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="hub-container"):
            with CardContainer(id="court-list"):
                pass

            yield CourtView()

        yield Footer()

    @on(CourtCard.Pressed)
    def on_court_card_pressed(self, event: CourtCard.Pressed) -> None:
        self.selected_court = event.court_card.court
