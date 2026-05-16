import requests

def fetch_data(url: str):
    """Fetches data from a URL with SSL verification."""
    # SAFE: verify=True
    return requests.get(url, verify=True)


def safe_divide(a: float, b: float) -> float:
    """Safely divides two numbers, returning 0 on error."""
    try:
        return a / b
    except Exception:
        return 0.0
