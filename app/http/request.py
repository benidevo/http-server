from dataclasses import dataclass, field
from typing import Any

from app.http.methods import HttpMethod
from app.utils import format_headers, parse_headers


@dataclass
class RequestMetadata:
    path_params: dict[str, str] = field(default_factory=dict)


@dataclass
class Request:
    method: HttpMethod
    version: str
    path: str
    headers: dict[str, str]
    body: str = field(default="")
    metadata: RequestMetadata = field(default_factory=lambda: RequestMetadata())

    @classmethod
    def deserialize(cls, request_str: str) -> "Request":
        request_line, headers, body = cls._parse_request(request_str)
        request_line_parts = request_line.split(" ")

        if len(request_line_parts) < 3:
            raise ValueError("Invalid request line format")

        method = HttpMethod(request_line_parts[0])
        path = request_line_parts[1]
        version = request_line_parts[2]

        return cls(
            method=method,
            version=version,
            path=path,
            headers=headers,
            body=body,
        )

    def serialize(self) -> str:
        headers = format_headers(self.headers)
        return f"{self.method} {self.path} {self.version}\r\n{headers}\r\n{self.body}"

    @staticmethod
    def _parse_request(request_str: str) -> tuple[str, dict[str, str], str]:
        parts = request_str.split("\r\n\r\n", 1)
        headers_section = parts[0]
        body = parts[1] if len(parts) > 1 else ""

        lines = headers_section.split("\r\n")
        request_line = lines[0]
        headers = parse_headers(lines[1:])

        return request_line, headers, body
