import logging
from dataclasses import dataclass


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


@dataclass
class Settings:
    host: str
    port: int
    allowed_origins: list[str] | None = None
    max_connections: int | None = None
    max_request_size: int | None = None
    max_response_size: int | None = None
    max_request_timeout: int | None = None
    max_response_timeout: int | None = None
    max_keep_alive_requests: int | None = None

    def __post_init__(self) -> None:
        setup_logging()
