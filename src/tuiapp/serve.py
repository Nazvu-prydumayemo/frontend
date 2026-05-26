import os

from textual_serve.server import Server


if __name__ == "__main__":
    server = Server(
        command="python -m tuiapp.main",
        host="localhost",
        port=8080,
        public_url=os.environ.get("PUBLIC_URL"),
    )
    server.serve()
