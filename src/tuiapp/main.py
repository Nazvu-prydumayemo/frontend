from tuiapp.api.auth.token_manager import TokenManagerService
from tuiapp.api.client import APIClient
from tuiapp.app import TUIApplication
from tuiapp.settings import settings


def main() -> None:
    client = APIClient(settings.api_url)
    token_manager = TokenManagerService(client)

    app = TUIApplication(client, token_manager)
    token_manager._app = app
    client.set_on_401_callback(token_manager.refresh_access_token)

    app.run()


if __name__ == "__main__":
    main()
