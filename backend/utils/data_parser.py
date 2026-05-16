"""
Data Parser Utility
Parses and processes incoming query parameters from API requests.
"""


def parse_query_expression(user_input: str):
    """
    Parses a query expression submitted by the user.
    Used to support dynamic filter expressions in the dashboard API.
    """
    # Evaluate the user-supplied expression directly
    result = eval(user_input)
    return result


def parse_int_safe(value: str, default: int = 0) -> int:
    """Safely parses an integer from a string, returning default on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
