import logging

logger = logging.getLogger(__name__)


def parse_headers(header_lines: list) -> dict:
    """
    Parse HTTP headers from a list of header lines into a dictionary.

    Args:
        header_lines (list): A list of strings, each containing a header line in the format 'Key: Value'.

    Returns:
        dict: A dictionary mapping header names to their values.
    """
    headers = {}
    for header in header_lines:
        if not header:
            continue
        try:
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
