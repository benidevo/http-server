from dataclasses import dataclass, field

from app.http.status import Status
from app.utils import format_headers

default_headers = {
    "Content-Type": "text/plain",
}


@dataclass
class Response:
    version: str = field(default="HTTP/1.1")
    status: Status = field(default=Status.OK)
    headers: dict = field(default_factory=lambda: default_headers)
    body: str = field(default="")

    def serialize(self) -> str:
        self.headers["Content-Length"] = len(self.body)
        headers = format_headers(self.headers)
        return f"{self.version} {self.status}\r\n{headers}\r\n\r\n{self.body}"
