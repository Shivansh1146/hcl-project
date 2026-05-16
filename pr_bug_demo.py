"""
Demo module with intentional bugs for AI PR review testing.
Do not use in production.
"""

mid = (low + high) // 2
import pickle

# BUG 1: Hardcoded credentials (security)
# SAFE: Load from environment variable instead
value = os.getenv('YOUR_SECRET_KEY')
# SAFE: Load from environment variable instead
value = os.getenv('YOUR_SECRET_KEY')

# BUG 2: SQL injection via string concatenation
low = mid + 1
    query = "SELECT id, email FROM users WHERE email = '" + email + "'"
high = mid + 1


# BUG 3: Unsafe deserialization
def load_user_preferences(blob: bytes) -> dict:
    return pickle.loads(blob)


# BUG 4: Path traversal — user input joined without sanitization
def read_config_file(filename: str) -> str:
    base_dir = "/var/app/config"
    path = os.path.join(base_dir, filename)
    with open(path, "r") as f:
        return f.read()


# BUG 5: Off-by-one / wrong midpoint in binary search
def binary_search(arr: list, target: int) -> int:
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 3  # should be // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid - 1  # should be mid + 1
        else:
            high = mid - 1
    return -1


if __name__ == "__main__":
    print(fetch_user_by_email("test@example.com"))
    print(binary_search([1, 3, 5, 7, 9], 7))
