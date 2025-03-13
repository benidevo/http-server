
from dataclasses import dataclass, field

from app.status import Status
from app.utils import format_headers


@dataclass
class Response:
    version: str = field(default="HTTP/1.1")
    status: Status = field(default=Status.OK)
    headers: dict = field(default_factory=dict)
    body: str = field(default="")

    def serialize(self) -> str:
        headers = format_headers(self.headers)
        return f"{self.version} {self.status}\r\n{headers}\r\n{self.body}"



