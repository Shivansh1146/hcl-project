import requests

def fetch_data(url: str):
    """Fetches data from a URL without SSL verification."""
    # BUG: verify=False is a security risk
    return requests.get(url, verify=False)


def safe_divide(a: float, b: float) -> float:
    """Safely divides two numbers, returning 0 on error."""
    try:
        return a / b
    except Exception:
        return 0.0
