from tuiapp.api.client import APIClient
from tuiapp.app import TUIApplication
from tuiapp.settings import settings


def main() -> None:
    app = TUIApplication(APIClient(settings.api_url))
    app.run()


if __name__ == "__main__":
    main()
