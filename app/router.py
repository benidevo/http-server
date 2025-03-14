from dataclasses import dataclass, field
from typing import Callable, Optional

from app.handler import BaseHandler

Routes = dict[str, Callable]


@dataclass
class Router:
    name: str = field(default="")
    routes: Routes = field(default_factory=lambda: {"/": BaseHandler()})

    def add_route(self, path: str, handler: Callable) -> None:
        self.routes[path] = handler()

    def route(self, path: str) -> Callable:
        return self.routes[path]

    def match_route(self, path: str) -> tuple[Optional[Callable], dict]:
        if path in self.routes:
            return self.routes[path], {}

        for pattern, handler in self.routes.items():
            path_params = self._match_pattern(pattern, path)
            if path_params is not None:
                return handler, path_params

        return None, {}

    def _match_pattern(self, pattern: str, path: str) -> dict | None:
        """
        Match a URL pattern with path parameters against an actual path.

        Matches patterns like "/users/{id}" against paths like "/users/123".
        Path parameters are extracted from {param} placeholders in the pattern.

        Args:
            pattern (str): URL pattern containing optional {param} placeholders
            path (str): Actual URL path to match against

        Returns:
            dict | None: Dictionary of extracted path parameters if pattern matches,
                        None if pattern does not match
        """
        pattern_parts = pattern.split("/")
        path_parts = path.split("/")

        if len(pattern_parts) != len(path_parts):
            return None

        params = {}
        for p_part, actual_part in zip(pattern_parts, path_parts):
            if p_part.startswith("{") and p_part.endswith("}"):
                param_name = p_part[1:-1]
                params[param_name] = actual_part
            elif p_part != actual_part:
                return None

        return params
