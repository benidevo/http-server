from demo.handlers import (
    EchoHandler,
    HomeHandler,
    InfoHandler,
    TimeHandler,
    TodoHandler,
    TodosHandler,
)
from app.server import HttpServer


def main() -> None:
    server = HttpServer(host="localhost", port=4221)

    server.router.add_route("/", HomeHandler)
    server.router.add_route("/info", InfoHandler)
    server.router.add_route("/time", TimeHandler)
    server.router.add_route("/echo/{message}", EchoHandler)
    server.router.add_route("/todos", TodosHandler)
    server.router.add_route("/todos/{id}", TodoHandler)

    server.run()


if __name__ == "__main__":
    main()
