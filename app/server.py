import logging
import socket
import threading
from dataclasses import dataclass

from app.configs import settings
from app.http.request import Request
from app.http.response import Response
from app.http.status import Status
from app.router import Router

logger = logging.getLogger(__name__)


@dataclass
class HttpConnection:
    connection: socket.socket
    address: str

    def send_response(self, response_bytes: bytes) -> None:
        self.connection.sendall(response_bytes)

    def set_timeout(self, timeout: int) -> None:
        self.connection.settimeout(timeout)

    def close(self) -> None:
        try:
            self.connection.close()
        except Exception:
            pass


class HttpServer:
    _THREAD_CLEANUP_INTERVAL: int = 5
    _THREAD_TIMEOUT: int = 1
    _CONNECTION_TIMEOUT: int = 30

    def __init__(self, host: str = settings.host, port: int = settings.port) -> None:
        self.host: str = host
        self.port: int = port
        self.socket = socket.create_server((self.host, self.port), reuse_port=True)
        self.router = Router()
        self.threads: list[threading.Thread] = []
        self.running: bool = False

    def run(self) -> None:
        """
        Run the HTTP server.

        Starts the server on the configured host and port, accepting incoming connections
        and handling them in separate threads. Also starts a cleanup thread to remove
        completed connection threads.

        The server runs until shutdown() is called or a KeyboardInterrupt is received.
        Each connection is handled in its own thread with configurable timeouts.
        """
        logger.info(f"Starting server on {self.host}:{self.port}")

        self.running = True
        cleanup_thread = threading.Thread(target=self._cleanup_threads, daemon=True)
        cleanup_thread.start()

        try:
            while self.running:
                try:
                    connection, address = self.socket.accept()
                    logger.info(f"Connection from {address}")

                    thread = threading.Thread(
                        target=self._handle_connection,
                        args=(connection, address),
                        daemon=True,
                    )
                    thread.start()
                    self.threads.append(thread)

                except (socket.error, socket.timeout) as e:
                    if self.running:
                        logger.error("Socket error: {e}")

        except KeyboardInterrupt:
            self.shutdown()

    def _handle_connection(self, connection: socket.socket, address: str) -> None:
        http_connection = HttpConnection(connection=connection, address=address)
        try:
            http_connection.set_timeout(self._CONNECTION_TIMEOUT)
            keep_alive = True

            while keep_alive and self.running:
                try:
                    request_data = b""
                    while True:
                        chunk = connection.recv(4096)
                        if not chunk:
                            break
                        request_data += chunk

                        if b"\r\n\r\n" in request_data:
                            break

                    if not request_data:
                        break

                    request_str = request_data.decode("utf-8")
                    logger.debug(f"Received request: {request_str}")

                    request: Request = Request.deserialize(request_str)
                    handler, path_params = self.router.match_route(request.path)

                    if handler is None:
                        response = Response(status=Status.NOT_FOUND)
                    else:
                        request.metadata.path_params.update(path_params)
                        response = handler(request)

                    connection_header = request.headers.get("Connection", "").lower()
                    keep_alive = connection_header == "keep-alive" and self.running

                    if keep_alive:
                        response.headers["Connection"] = "keep-alive"
                    else:
                        response.headers["Connection"] = "close"

                    http_connection.send_response(response.serialize())

                except socket.timeout:
                    logger.info(f"Connection from {address} timed out")
                    keep_alive = False

                except Exception as e:
                    logger.error(f"Error handling request: {e}")
                    http_connection.send_response(
                        Response(status=Status.INTERNAL_SERVER_ERROR).serialize()
                    )

        finally:
            http_connection.close()
            logger.info(f"Connection from {address} closed")

    def shutdown(self) -> None:
        """
        Gracefully shuts down the server.

        Sets the running flag to False, closes the server socket, and waits for all client
        connection threads to complete. Times out thread joins after self._THREAD_TIMEOUT seconds.
        """
        logger.info("Shutting down server...")

        self.running = False
        try:
            self.socket.close()
        except Exception:
            pass

        for thread in self.threads:
            thread.join(timeout=self._THREAD_TIMEOUT)
        logger.info("Server stopped")

    def _cleanup_threads(self) -> None:
        while self.running:
            self.threads = [thread for thread in self.threads if thread.is_alive()]

            threading.Event().wait(self._THREAD_CLEANUP_INTERVAL)
