from app.configs import settings
from app.demo.handlers import EchoHandler, UserAgentHandler
from app.server import HttpServer


def main() -> None:
    server = HttpServer(settings.host, settings.port)
    server.router.add_route("/echo/{str}", EchoHandler)
    server.router.add_route("/user-agent", UserAgentHandler)
    server.run()


if __name__ == "__main__":
    main()
