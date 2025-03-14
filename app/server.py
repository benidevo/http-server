import logging
import socket
from dataclasses import dataclass

from app.request import Request
from app.response import Response
from app.router import Router
from app.status import Status

logger = logging.getLogger(__name__)


@dataclass
class HttpConnection:
    connection: socket.socket
    address: str

    def send_response(self, response_str: str) -> None:
        self.connection.sendall(response_str.encode("utf-8"))
        self.connection.close()


class HttpServer:
    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = port
        self.connections: list[HttpConnection] = []
        self.socket = socket.create_server((self.host, self.port), reuse_port=True)
        self.router = Router()

    def run(self) -> None:
        """
        Starts the server and begins listening for incoming connections.

        This method initializes the server and enters the main server loop.
        It continuously listens for and handles incoming client requests until
        interrupted. The server can be stopped by sending a KeyboardInterrupt
        (Ctrl+C).

        The method logs when the server starts, any errors that occur while
        handling requests, and when the server is shutting down.

        Raises:
            KeyboardInterrupt: When the server is manually stopped
            Exception: If an error occurs while handling a request
        """
        logger.info(f"Starting server on {self.host}:{self.port}")

        while True:
            try:
                self.handle_request()
            except KeyboardInterrupt:
                logger.info("Shutting down server...")
                break
            except Exception as e:
                logger.error(f"Error handling request: {e}")

    def handle_request(self) -> None:
        connection, address = self.socket.accept()
        logger.info(f"Connection from {address}")

        http_connection = HttpConnection(connection=connection, address=address)
        self.connections.append(http_connection)

        request_str = connection.recv(1024).decode("utf-8")
        logger.info(f"Received request: {request_str}")

        request: Request = Request.deserialize(request_str)
        handler, path_params = self.router.match_route(request.path)

        if handler is None:
            response = Response(status=Status.NOT_FOUND)
            http_connection.send_response(response.serialize())
            return

        logger.debug(f"Routing request to {request.path} with params {path_params}")

        request.metadata.path_params.update(path_params)

        response = handler(request)
        http_connection.send_response(response.serialize())

    def shutdown(self) -> None:
        logger.info("Shutting down server...")
        for connection in self.connections:
            connection.connection.close()
        self.socket.close()
        logger.info("Server stopped")
