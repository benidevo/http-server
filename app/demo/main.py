from app.demo.handlers import EchoHandler, FileHandler, UserAgentHandler
from app.server import HttpServer


def run_demo() -> None:
    server = HttpServer()
    server.router.add_route("/echo/{str}", EchoHandler)
    server.router.add_route("/user-agent", UserAgentHandler)
    server.router.add_route("/files/{file_path}", FileHandler)
    server.run()
