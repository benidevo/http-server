# Python HTTP Server

A lightweight, modular HTTP/1.1 server implementation in Python. This project implements a complete HTTP server from scratch, following HTTP/1.1 specifications with a focus on clean architecture and extensibility.

> **Note**: This project is for educational purposes only and not intended for production use.

## Features

- **Complete HTTP/1.1 Implementation**: Full request and response handling with proper protocol compliance
- **Modular Architecture**: Clean separation of concerns through well-defined components
- **Type-Safe Implementation**: Comprehensive type annotations and static type checking
- **Extensible Routing System**: Support for path parameters and pattern matching
- **Handler-Based Endpoints**: Class-based handlers with method-specific processing
- **Content Compression**: Built-in support for gzip response compression
- **Connection Management**: Support for keep-alive connections and proper thread handling
- **Configurable Settings**: Easily customizable server behavior

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pipenv (for dependency management)

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/benidevo/http-server.git
   cd http-server
   ```

2. Install dependencies:

   ```
   pipenv install
   ```

3. Install development dependencies (optional):

   ```
   pipenv install --dev
   ```

### Running the Server

Start the server using the provided run script:

```
sh run.sh
```

Or use the Make command:

```
make start
```

The server will start on `localhost:4221` by default (configurable in `app/configs/__init__.py`).

## Usage

### Creating a New Server

```python
from app.server import HttpServer
from app.handler import BaseHandler
from app.http.request import Request
from app.http.response import Response

# Create a custom handler
class HelloHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        return Response(body="Hello, World!")

# Initialize the server
server = HttpServer(host="localhost", port=8080)

# Register routes
server.router.add_route("/", HelloHandler)

# Start the server
server.run()
```

### Path Parameters

The router supports path parameters with the `{param}` syntax:

```python
class UserHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        user_id = request.metadata.path_params.get("id")
        return Response(body=f"User ID: {user_id}")

# Register with parameter
server.router.add_route("/users/{id}", UserHandler)
```

### HTTP Methods

The `BaseHandler` class provides default implementations for common HTTP methods:

```python
class ResourceHandler(BaseHandler):
    def get(self, request: Request) -> Response:
        return Response(body="GET request")

    def post(self, request: Request) -> Response:
        return Response(body="POST request")

    def put(self, request: Request) -> Response:
        return Response(body="PUT request")

    def delete(self, request: Request) -> Response:
        return Response(body="DELETE request")
```

## Design Decisions

### Handler-Based Architecture

The server uses a class-based handler system inspired by frameworks like Flask and Django. This design allows for:

- Method-specific request handling with a clean API
- Shared logic through class inheritance
- Intuitive mapping of HTTP methods to handler methods

### Thread Per Connection

Each client connection is handled in a separate thread, allowing for:

- Concurrent request processing
- Isolation between client connections
- Simple implementation with Python's threading library

### Strong Type Safety

The implementation uses:

- Type annotations throughout the codebase
- Strict mypy configuration for static type checking
- Dataclasses for clean, typed data structures

### Response Compression

The server implements automatic gzip compression when clients indicate support, improving:

- Response bandwidth efficiency
- Compatibility with modern clients
- Performance for text-heavy responses

## Demo Application

The included demo application (`demo/main.py`) showcases:

- Basic routing
- Handler implementation
- Path parameter extraction
- JSON request/response handling
- A simple RESTful TODO API

To test the demo endpoints:

```
# Get server info
curl http://localhost:4221/info

# Create a TODO item
curl -X POST http://localhost:4221/todos -d '{"title": "New task", "completed": false}'

# Get all TODOs
curl http://localhost:4221/todos

# Get a specific TODO
curl http://localhost:4221/todos/1
```
