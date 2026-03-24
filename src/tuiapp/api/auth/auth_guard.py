from textual import on
from textual.events import Mount

from tuiapp.api.account.schema import MeResponse


class AuthGuard:
    user: MeResponse | None = None

    @on(Mount)
    async def _auth_guard(self) -> None:
        user = await self.app.account.me()  # type: ignore
        if user is None:
            self.app.pop_screen()  # type: ignore
            self.app.push_screen("main")  # type: ignore
            return

        self.user = user
