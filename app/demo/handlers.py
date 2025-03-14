import logging

from app.handler import BaseHandler
from app.http.request import Request
from app.http.response import Response
from app.http.status import Status

logger = logging.getLogger(__name__)


class EchoHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        path = request.metadata.path_params.get("str", "Hello, World!")
        return Response(body=path)


class UserAgentHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        user_agent = request.headers.get(
            "User-Agent", request.headers.get("user-agent", "Unknown")
        )
        return Response(body=user_agent)
