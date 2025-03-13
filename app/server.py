import logging
import socket
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from app.request import Request
from app.response import Response
from app.router import Router
from app.status import Status

log = logging.getLogger(__name__)


class Server(ABC):
    @abstractmethod
    def __enter__(self) -> "Server":
        """
        Context manager entry point to start the server.

        This method should start the server and make it ready to accept
        connections. It should also return the object itself, so that the
        context manager can return it properly.

        Returns:
            The server object itself.
        """
        raise NotImplementedError

    @abstractmethod
    def __exit__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """
        Starts the server and begins accepting connections.

        This method should be implemented to initialize and run the server,
        setting it up to handle incoming client requests. The implementation
        should ensure that the server is ready to accept connections and
        handle them appropriately.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """
        Stops the server and closes any open connections.

        This method should be implemented to properly shut down the server,
        closing any open connections and releasing any resources that were
        allocated.
        """
        raise NotImplementedError

    @abstractmethod
    def handle_request(self) -> None:
        """
        Handles a single incoming request.

        This method should be implemented to handle an individual
        incoming request from a client. It should be responsible for
        reading the request from the client, processing it, and
        sending a response back to the client.

        The implementation should be responsible for managing the
        lifetime of the client connection and properly closing it
        when the request is finished being handled.
        """
        raise NotImplementedError


@dataclass
class HttpConnection:
    connection: socket.socket
    address: str

    def send_response(self, response_str: str) -> None:
        self.connection.sendall(response_str.encode("utf-8"))
        self.connection.close()


class HttpServer(Server):
    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = port
        self.connections: list[HttpConnection] = []
        self.socket = socket.create_server((self.host, self.port), reuse_port=True)
        self.router = Router()

    def run(self) -> None:
        log.info(f"Starting server on {self.host}:{self.port}")

        while True:
            try:
                self.handle_request()
            except KeyboardInterrupt:
                log.info("Shutting down server...")
                break
            except Exception as e:
                log.error(f"Error handling request: {e}")

    def handle_request(self) -> None:
        connection, address = self.socket.accept()
        log.info(f"Connection from {address}")

        http_connection = HttpConnection(connection=connection, address=address)
        self.connections.append(http_connection)

        request_str = connection.recv(1024).decode("utf-8")
        log.info(f"Received request: {request_str}")

        request: Request = Request.deserialize(request_str)
        if request.path not in self.router.routes:
            response = Response(
                status=Status.NOT_FOUND,
            )
            http_connection.send_response(response.serialize())
            return
        log.info(f"Routing request to {request.__dict__}")

        handler = self.router.routes[request.path]
        response = handler(request)
        http_connection.send_response(response.serialize())

    def __enter__(self) -> "HttpServer":
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        self.stop()
        log.info("Server stopped")

    def stop(self) -> None:
        for connection in self.connections:
            connection.connection.close()
        self.socket.close()
