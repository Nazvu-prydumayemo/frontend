from textual import on
from textual.events import Mount

from tuiapp.api.account.schema import User, UserResult


class AuthGuard:
    user: User | None = None

    async def _auth_guard(self) -> None:
        await self._fetch_user()

    @on(Mount)
    async def _on_mount(self) -> None:
        await self._fetch_user()

    async def _fetch_user(self) -> None:
        result: UserResult = await self.app.account.me()  # type: ignore
        if result.user is None or result.status != "success":
            self.app.pop_screen()  # type: ignore
            self.app.push_screen("main")  # type: ignore
            return

        self.user = result.user
