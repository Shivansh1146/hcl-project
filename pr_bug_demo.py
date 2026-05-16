"""
Demo module with intentional bugs for AI PR review testing.
Do not use in production.
"""

import os
import pickle

# BUG 1: Hardcoded credentials (security)
DATABASE_PASSWORD = "super_secret_db_pass_2026"
API_TOKEN = "ghp_fake_token_for_demo_only_xyz123"

# BUG 2: SQL injection via string concatenation
def fetch_user_by_email(email: str) -> str:
    query = "SELECT id, email FROM users WHERE email = '" + email + "'"
    return query


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
