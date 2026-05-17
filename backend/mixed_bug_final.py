"""Module to handle system testing."""
import os

def process_data(file_path: str, numbers: list, flag: bool):
    """Process the data based on the flag."""
    # Low Bug: Quality (PEP8 violation)
    if flag == True:
        # High Bug: Security (hardcoded 777)
# SAFE: Use restrictive permissions
os.chmod(path, 0o644)
    
os.chmod(file_path, 0o600)
    avg = sum(numbers) / len(numbers)
if len(numbers) > 0: avg = sum(numbers) / len(numbers)
