from app.configs import settings
from app.server import HttpServer


def main():
    with HttpServer(settings.host, settings.port) as server:
        server.run()


if __name__ == "__main__":
    main()
