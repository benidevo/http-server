import logging
from collections import namedtuple
from typing import Callable

from app.http.request import Request
from app.http.response import Response
from app.http.status import Status

logger = logging.getLogger(__name__)

RouteParams = namedtuple("RouteParams", ["path_params", "query_params"])


class BaseHandler:
    _METHODS_MAP = {
        "GET": "get",
        "POST": "post",
        "PUT": "put",
        "DELETE": "delete",
    }

    def __call__(self, request: Request) -> Response:
        method = self._METHODS_MAP[request.method]
        method_func: Callable[[Request], Response] | None = getattr(self, method, None)
        if method_func is None:
            return Response(status=Status.METHOD_NOT_ALLOWED)
        return method_func(request)

    def get(self, request: Request) -> Response:
        """Handles GET requests.

        Args:
            request (Request): The incoming HTTP request object containing the request
                details including path parameters, query parameters, headers, and body.

        Returns:
            Response: A Response object with HTTP 200 OK status code. By default returns
                an empty response body. Subclasses should override this method to provide
                specific GET request handling.
        """
        return Response(status=Status.OK)

    def post(self, request: Request) -> Response:
        """Handles POST requests.

        Args:
            request (Request): The incoming HTTP request object containing the request
                details including path parameters, query parameters, headers, and body.

        Returns:
            Response: A Response object with HTTP 405 Method Not Allowed status code.
                Subclasses should override this method to provide specific POST request
                handling.
        """
        return Response(status=Status.METHOD_NOT_ALLOWED)

    def put(self, request: Request) -> Response:
        """Handles PUT requests.

        Args:
            request (Request): The incoming HTTP request object containing the request
                details including path parameters, query parameters, headers, and body.

        Returns:
            Response: A Response object with HTTP 405 Method Not Allowed status code.
                Subclasses should override this method to provide specific PUT request
                handling.
        """
        return Response(status=Status.METHOD_NOT_ALLOWED)

    def patch(self, request: Request) -> Response:
        """Handles PATCH requests.

        Args:
            request (Request): The incoming HTTP request object containing the request
                details including path parameters, query parameters, headers, and body.

        Returns:
            Response: A Response object with HTTP 405 Method Not Allowed status code.
                Subclasses should override this method to provide specific PATCH request
                handling.
        """
        return Response(status=Status.METHOD_NOT_ALLOWED)

    def delete(self, request: Request) -> Response:
        """Handles DELETE requests.

        Args:
            request (Request): The incoming HTTP request object containing the request
                details including path parameters, query parameters, headers, and body.

        Returns:
            Response: A Response object with HTTP 405 Method Not Allowed status code.
                Subclasses should override this method to provide specific DELETE request
                handling.
        """
        return Response(status=Status.METHOD_NOT_ALLOWED)
