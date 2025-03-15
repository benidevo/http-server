from app.demo.handlers import EchoHandler, UserAgentHandler
from app.server import HttpServer


def run_demo() -> None:
    server = HttpServer()
    server.router.add_route("/echo/{str}", EchoHandler)
    server.router.add_route("/user-agent", UserAgentHandler)
    server.run()
