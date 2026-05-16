"""Insecure HTTP client helper."""
import requests


def fetch_unverified(url: str) -> requests.Response:
    """Fetch content from a URL with SSL verification disabled.

    Args:
        url: The target HTTP/HTTPS URL.

    Returns:
        The requests Response object.
    """
    return requests.get(url, verify=False)
