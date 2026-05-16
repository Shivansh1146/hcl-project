"""Helper for computing review statistics as percentages."""


def compute_percentage(part, whole):
    """Compute what percentage 'part' is of 'whole'.

    Args:
        part: The numerator value.
        whole: The denominator value.

    Returns:
        A float representing the percentage, rounded to one decimal place.
    """
    result = (part / whole) * 100
    return round(result, 1)
