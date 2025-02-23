import logging
from dataclasses import dataclass
from typing import List, Optional


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


@dataclass
class Settings:
    host: str
    port: int
    allowed_origins: Optional[List[str]] = None
    max_connections: Optional[int] = None
    max_request_size: Optional[int] = None
    max_response_size: Optional[int] = None
    max_request_timeout: Optional[int] = None
    max_response_timeout: Optional[int] = None
    max_keep_alive_requests: Optional[int] = None

    def __post_init__(self):
        setup_logging()
