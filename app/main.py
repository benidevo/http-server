from app.configs import settings
from app.demo.handlers import EchoHandler
from app.server import HttpServer


def main() -> None:
    server = HttpServer(settings.host, settings.port)
    server.router.add_route("/echo/{str}", EchoHandler)
    server.run()


if __name__ == "__main__":
    main()
