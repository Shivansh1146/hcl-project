"""
Utility module for the AI Code Reviewer backend.

Provides helper functions for date formatting, text sanitization,
and structured logging used across the application.
"""

import re
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger("backend.utils")


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Return an ISO-8601 UTC timestamp string.

    Args:
        dt: A datetime object. Defaults to the current UTC time.

    Returns:
        A string in ISO-8601 format with timezone info.
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.isoformat()


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to a maximum length with an ellipsis indicator.

    Args:
        text: The input string to truncate.
        max_length: Maximum allowed character count (must be >= 4).

    Returns:
        The original string if within limits, otherwise truncated
        with a trailing ellipsis.
    """
    if not isinstance(text, str):
        return ""
    if max_length < 4:
        max_length = 4
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def sanitize_filename(name: str) -> str:
    """Remove characters that are unsafe for filesystem paths.

    Keeps alphanumeric characters, hyphens, underscores, and dots.

    Args:
        name: The raw filename string.

    Returns:
        A sanitized filename string safe for use on all major OSes.
    """
    if not isinstance(name, str):
        return ""
    cleaned = re.sub(r"[^\w\-.]", "_", name)
    # Collapse consecutive underscores
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned.strip("_")


def build_log_context(pr_number: int, repo: str, action: str) -> str:
    """Create a structured log prefix for consistent log formatting.

    Args:
        pr_number: The pull request number.
        repo: The repository full name (owner/repo).
        action: A short description of the current action.

    Returns:
        A formatted string suitable as a log message prefix.
    """
    timestamp = format_timestamp()
    return f"[{timestamp}] PR #{pr_number} | {repo} | {action}"


def calculate_coverage_percent(processed: int, total: int) -> float:
    """Compute analysis coverage as a percentage.

    Args:
        processed: Number of chunks successfully analyzed.
        total: Total number of chunks in the diff.

    Returns:
        A float between 0.0 and 100.0 representing coverage.
        Returns 100.0 when total is zero (nothing to analyze).
    """
    if total <= 0:
        return 100.0
    percentage = (processed / total) * 100
    return round(min(percentage, 100.0), 1)
