# Python HTTP Server

A lightweight, modular HTTP/1.1 server implementation in Python. This project implements a basic HTTP server from scratch, following HTTP/1.1 specifications to handle client requests.

> **Note**: This project is for educational purposes only and not intended for production use. It is currently a work in progress as features are being implemented incrementally.

## Features

- Complete HTTP/1.1 request and response handling
- Modular architecture with clean separation of concerns
- Type-safe implementation with comprehensive type annotations
- Configurable server settings
- Extensible routing system
- Support for standard HTTP methods (GET, POST, PUT, DELETE, etc.)


### Key Components

- **Server**: Core HTTP server implementation with connection handling
- **Router**: Request routing to appropriate handlers
- **Request/Response**: HTTP message parsing and serialization
- **Methods/Status**: Enums for HTTP methods and status codes
- **Configs**: Server configuration management

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pipenv (for dependency management)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/benidevo/http-server
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

## Development

### Code Formatting and Linting

The project uses:
- Black for code formatting
- isort for import sorting
- mypy for static type checking

Run formatting and linting:

```
make format  # Format code
make lint    # Format and type-check code
```


## Architecture

### Request Flow

1. Client sends HTTP request to server
2. Server parses the request into a `Request` object
3. Router matches the request path to a handler
4. Handler processes the request and returns a `Response`
5. Server serializes and sends the response back to the client

### Main Components

- **HttpServer**: Manages socket connections and request handling
- **Router**: Maps URL paths to handler functions
- **Request/Response**: Data models for HTTP messages
- **HttpMethod/Status**: Enumerations for HTTP protocol values
