from tuiapp.api.auth.token_manager import TokenManagerService
from tuiapp.api.client import APIClient
from tuiapp.app import TUIApplication
from tuiapp.settings import settings


def create_app() -> TUIApplication:
    client = APIClient(settings.api_url)
    token_manager = TokenManagerService(client)

    app = TUIApplication(client, token_manager)
    token_manager._app = app
    client.set_on_401_callback(token_manager.refresh_access_token)

    return app


def main() -> None:
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
