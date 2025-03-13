from enum import StrEnum


class Status(StrEnum):
    OK = "200 OK"
    CREATED = "201 Created"
    ACCEPTED = "202 Accepted"
    NO_CONTENT = "204 No Content"
    PARTIAL_CONTENT = "206 Partial Content"
    MULTIPLE_CHOICES = "300 Multiple Choices"
    MOVED_PERMANENTLY = "301 Moved Permanently"
    FOUND = "302 Found"
    NOT_FOUND = "404 Not Found"
    INTERNAL_SERVER_ERROR = "500 Internal Server Error"
    NOT_IMPLEMENTED = "501 Not Implemented"
    BAD_REQUEST = "400 Bad Request"
    FORBIDDEN = "403 Forbidden"
