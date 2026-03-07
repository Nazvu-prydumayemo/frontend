from tuiapp.api.client import APIClient
from tuiapp.app import TUIApplication
from tuiapp.settings import settings


def main() -> None:
    app = TUIApplication(APIClient(settings.api_url, settings.api_token))
    app.run()


if __name__ == "__main__":
    main()
