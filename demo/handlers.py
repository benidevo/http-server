import json
import logging
from datetime import datetime

from app.handler import BaseHandler
from app.http.request import Request
from app.http.response import Response
from app.http.status import Status

logger = logging.getLogger(__name__)


TODOS: dict[str, dict] = {
    "1": {"id": "1", "title": "Learn HTTP", "completed": True},
    "2": {"id": "2", "title": "Build a server", "completed": True},
    "3": {"id": "3", "title": "Test the server", "completed": False},
}


class HomeHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>HTTP Server Demo</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                .endpoint { background: #f4f4f4; padding: 10px; margin: 10px 0; border-radius: 5px; }
                code { background: #e0e0e0; padding: 2px 4px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>HTTP Server Demo</h1>
            <p>Welcome to the HTTP server demo! Here are the available endpoints:</p>

            <div class="endpoint">
                <h3>GET /</h3>
                <p>This page</p>
            </div>

            <div class="endpoint">
                <h3>GET /info</h3>
                <p>Server information and request details</p>
            </div>

            <div class="endpoint">
                <h3>GET /time</h3>
                <p>Current server time</p>
            </div>

            <div class="endpoint">
                <h3>GET /echo/{message}</h3>
                <p>Echoes back the message in the URL</p>
            </div>

            <div class="endpoint">
                <h3>GET /todos</h3>
                <p>List all TODOs</p>
            </div>

            <div class="endpoint">
                <h3>GET /todos/{id}</h3>
                <p>Get a specific TODO by ID</p>
            </div>

            <div class="endpoint">
                <h3>POST /todos</h3>
                <p>Create a new TODO (send JSON body)</p>
            </div>

            <div class="endpoint">
                <h3>PUT /todos/{id}</h3>
                <p>Update a TODO (send JSON body)</p>
            </div>

            <div class="endpoint">
                <h3>DELETE /todos/{id}</h3>
                <p>Delete a TODO</p>
            </div>
        </body>
        </html>
        """
        return Response(body=html, headers={"Content-Type": "text/html"})


class InfoHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        info = {
            "server": "Python HTTP Server Demo",
            "time": datetime.now().isoformat(),
            "request": {
                "method": str(request.method),
                "path": request.path,
                "headers": dict(request.headers),
            },
        }
        return Response(
            body=json.dumps(info, indent=2),
            headers={"Content-Type": "application/json"},
        )


class TimeHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        return Response(body=datetime.now().isoformat())


class EchoHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        message = request.metadata.path_params.get("message", "No message provided")
        return Response(body=message)


class TodosHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        return Response(
            body=json.dumps(list(TODOS.values()), indent=2),
            headers={"Content-Type": "application/json"},
        )

    def post(self, request: Request) -> Response:
        try:
            todo = json.loads(request.body)
            todo_id = str(max(int(id) for id in TODOS.keys()) + 1)
            todo["id"] = todo_id
            TODOS[todo_id] = todo

            return Response(
                status=Status.CREATED,
                body=json.dumps(todo, indent=2),
                headers={"Content-Type": "application/json"},
            )
        except (json.JSONDecodeError, ValueError) as e:
            return Response(status=Status.BAD_REQUEST, body=f"Invalid JSON: {str(e)}")


class TodoHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        todo_id = request.metadata.path_params.get("id", "")
        todo = TODOS.get(todo_id)

        if not todo:
            return Response(
                status=Status.NOT_FOUND, body=f"Todo with ID {todo_id} not found"
            )

        return Response(
            body=json.dumps(todo, indent=2),
            headers={"Content-Type": "application/json"},
        )

    def put(self, request: Request) -> Response:
        todo_id = request.metadata.path_params.get("id", "")
        if todo_id not in TODOS:
            return Response(
                status=Status.NOT_FOUND, body=f"Todo with ID {todo_id} not found"
            )

        try:
            updated_todo = json.loads(request.body)
            updated_todo["id"] = todo_id
            TODOS[todo_id] = updated_todo

            return Response(
                body=json.dumps(updated_todo, indent=2),
                headers={"Content-Type": "application/json"},
            )
        except json.JSONDecodeError:
            return Response(status=Status.BAD_REQUEST, body="Invalid JSON")

    def delete(self, request: Request) -> Response:
        todo_id = request.metadata.path_params.get("id", "")
        if todo_id not in TODOS:
            return Response(
                status=Status.NOT_FOUND, body=f"Todo with ID {todo_id} not found"
            )

        del TODOS[todo_id]
        return Response(status=Status.NO_CONTENT)
