from dataclasses import dataclass, field
from typing import Callable

from app.request import Request
from app.response import Response
from app.status import Status


class DefaultHandler:
    def __call__(self, request: Request) -> Response:
        return Response(status=Status.OK)


Routes = dict[str, Callable]


@dataclass
class Router:
    name: str = field(default="")
    routes: Routes = field(default_factory=lambda: {"/": DefaultHandler()})

    def add_route(self, path: str, handler: Callable) -> None:
        self.routes[path] = handler

    def route(self, path: str) -> Callable:
        return self.routes[path]
