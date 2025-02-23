import logging
import socket
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

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
    def __exit__(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        """
        Starts the server and begins accepting connections.

        This method should be implemented to initialize and run the server,
        setting it up to handle incoming client requests. The implementation
        should ensure that the server is ready to accept connections and
        handle them appropriately.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """
        Stops the server and closes any open connections.

        This method should be implemented to properly shut down the server,
        closing any open connections and releasing any resources that were
        allocated.
        """
        raise NotImplementedError

    @abstractmethod
    def handle_request(self):
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

    def send_response(self, response: str):
        self.connection.sendall(response.encode("utf-8"))
        self.connection.close()


@dataclass
class HttpResponse:
    connection: HttpConnection
    status_line: str
    headers: Optional[str] = ""
    body: Optional[str] = ""

    def send(self):
        response = f"{self.status_line}\r\n{self.headers}\r\n\r\n{self.body}"
        try:
            self.connection.send_response(response)
        except Exception as e:
            log.error(f"Error encoding response body: {e}")


class HttpServer(Server):
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        self.connections: Optional[List[HttpConnection]] = None
        self.socket: Optional[socket.socket] = None

    def run(self):
        log.info(f"Starting server on {self.host}:{self.port}")
        if not self.socket:
            self.socket = socket.create_server((self.host, self.port), reuse_port=True)
            self.connections = []

        while True:
            try:
                self.handle_request()
            except KeyboardInterrupt:
                log.info("Shutting down server...")
                break
            except Exception as e:
                log.error(f"Error handling request: {e}")

    def handle_request(self):
        connection, address = self.socket.accept()
        log.info(f"Connection from {address}")

        request = connection.recv(1024).decode("utf-8")
        log.info(f"Received request: {request}")

        http_connection = HttpConnection(connection=connection, address=address)
        self.connections.append(http_connection)
        response = HttpResponse(
            connection=http_connection,
            status_line="HTTP/1.1 200 OK",
            headers="Content-Type: text/html",
            body="<html><body>Hello, World!</body></html>",
        )
        response.send()

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        log.info("Server stopped")

    def stop(self):
        for connection in self.connections:
            connection.connection.close()
        self.socket.close()
