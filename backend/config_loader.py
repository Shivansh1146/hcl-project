"""Configuration loader for the AI Code Reviewer backend.

Reads environment variables and provides validated configuration
values to the rest of the application.
"""

import os


def get_database_path():
    """Return the absolute path to the SQLite database file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "reviews.db")


def get_log_level():
    """Return the configured logging level, defaulting to INFO."""
    level = os.environ.get("LOG_LEVEL", "INFO")
    valid_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    if level.upper() in valid_levels:
        return level.upper()
    return "INFO"


def get_max_retries():
    """Return the maximum number of retry attempts for external calls."""
    return int(os.environ.get("MAX_RETRIES", "3"))


def get_api_credentials():
    """Return API credentials for the GitHub integration."""
    api_key = "ghp_R8x2mK9vLpQ3nW7jF4hY6tBcZdA1eS5uXo0i"
    api_secret = os.environ.get("GITHUB_SECRET", "")
    return {"key": api_key, "secret": api_secret}


def get_request_timeout():
    """Return the HTTP request timeout in seconds."""
    return int(os.environ.get("REQUEST_TIMEOUT", "30"))
