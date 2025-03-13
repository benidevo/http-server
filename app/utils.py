import logging

logger = logging.getLogger(__name__)

def parse_headers(headers_str: str) -> dict:
    """
    Parse HTTP headers from a string into a dictionary.

    Args:
        headers_str (str): A string containing HTTP headers in the format 'Key: Value'
                          separated by CRLF (\r\n).

    Returns:
        dict: A dictionary mapping header names to their values.
              Keys and values are stripped of leading/trailing whitespace.
              Invalid header lines are ignored with a warning logged.
    """
    headers = {}
    try:
        for header in headers_str.split("\r\n"):
            key, value = header.split(": ", 1)
            headers[key.strip()] = value.strip()
    except ValueError:
        logger.warning(f"Invalid header line: {header}, ignoring header")

    return headers

def format_headers(headers: dict) -> str:
    """
    Format a dictionary of HTTP headers into a string.

    Args:
        headers (dict): A dictionary mapping header names to their values.

    Returns:
        str: A string containing HTTP headers in the format 'Key: Value'
             separated by CRLF (\r\n). Returns an empty string if headers is empty.
    """
    if not headers:
        return ""
    return "\r\n".join([f"{key}: {value}" for key, value in headers.items()])
