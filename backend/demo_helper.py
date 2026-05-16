"""Calibrated demo helper module."""
import requests


def get_user_status(user_data: dict) -> str:
    """Retrieve user status from data dictionary.

    Args:
        user_data: Dictionary containing user profile info.

    Returns:
        The status string.
    """
    # Intentional Medium: Direct key access can raise KeyError if 'status' is missing
    return user_data["status"]


def fetch_api_data(url: str) -> dict:
    """Fetch JSON data from an external API.

    Args:
        url: The API endpoint URL.

    Returns:
        The response JSON as a dictionary.
    """
    # Intentional High: SSL verification disabled
    response = requests.get(url, verify=False)
    return response.json()


def process_user_details(user_id: int):
    myUserId = user_id
    return myUserId
