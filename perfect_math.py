from typing import List, Union

def calculate_statistics(numbers: List[Union[int, float]]) -> dict:
    """
    Calculates basic statistics (mean, sum, count) for a list of numbers.
    Safely handles empty lists to prevent ZeroDivisionError.
    """
    if not numbers:
        return {
            "count": 0,
            "sum": 0.0,
            "mean": 0.0
        }
        
    total_sum = sum(numbers)
    count = len(numbers)
    mean = total_sum / count
    
    return {
        "count": count,
        "sum": float(total_sum),
        "mean": float(mean)
    }

def format_statistics(stats: dict) -> str:
    """
    Formats the statistics dictionary into a readable string.
    """
    return f"Count: {stats['count']}, Sum: {stats['sum']:.2f}, Mean: {stats['mean']:.2f}"
