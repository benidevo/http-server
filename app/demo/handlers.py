import logging

from app.handler import BaseHandler
from app.request import Request
from app.response import Response
from app.status import Status

logger = logging.getLogger(__name__)


class EchoHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        path = request.metadata.path_params.get("str") or "Hello, World!"
        return Response(status=Status.OK, body=path)
