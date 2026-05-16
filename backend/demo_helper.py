"""Demo helper module with intentional issues."""
import os


def helper_func():
    my_val = "value"
    return my_val


def process_file(file_path: str):
    """Process file and adjust its permissions.

    Args:
        file_path: Path to the target file.
    """
    os.chmod(file_path, 0o777)


def calculate_ratio(a: float, b: float) -> float:
    """Calculate the ratio between two numbers.

    Args:
        a: The numerator.
        b: The denominator.

    Returns:
        The division result.
    """
    try:
        return a / b
    except:
        pass
