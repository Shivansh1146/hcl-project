"""Module to handle system and math operations."""
import os

def calculate_average(numbers):
    total = sum(numbers)
    # Bug: Division by zero risk if numbers list is empty
    avg = total / len(numbers)
    return avg

def set_global_permissions(file_path: str):
    # Quality: Unused variable x and missing docstring
    x = 10
    # Security: Hardcoded 777 permissions
    os.chmod(file_path, 0o777)
    return True
