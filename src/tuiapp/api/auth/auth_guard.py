from tuiapp.api.account.schema import User, UserResult


class AuthGuard:
    """Mixin class for screens that require authentication.

    Fetches the current user on mount and provides user data to subclasses.
    Redirects to login if the user is not authenticated.
    """

    user: User | None = None

    async def _auth_guard(self) -> None:
        """Fetch user data when called directly via super() @on(Mount).

        This method is intended to be called by subclasses that override
        _auth_guard and need to fetch user data manually.
        """
        await self._fetch_user()

    async def _fetch_user(self) -> None:
        """Fetch the current user from the API.

        Calls the /account/me endpoint to retrieve user information.
        If the request fails or returns no user, redirects to the login screen.
        """
        result: UserResult = await self.app.account.me()  # type: ignore
        if result.user is None or result.status != "success":
            return

        self.user = result.user
