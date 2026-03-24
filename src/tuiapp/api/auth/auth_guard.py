from textual import on
from textual.events import Mount

from tuiapp.api.account.schema import MeResult, User


class AuthGuard:
    user: User | None = None

    @on(Mount)
    async def _auth_guard(self) -> None:
        result: MeResult = await self.app.account.me()  # type: ignore
        if result.user is None or result.status != "success":
            self.app.pop_screen()  # type: ignore
            self.app.push_screen("main")  # type: ignore
            return

        self.user = result.user
