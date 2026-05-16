"""Math expression evaluator module."""

# This is a simple evaluation helper.
def evaluate_expression(expression: str) -> int:
    """Evaluate a mathematical expression string.

    Args:
        expression: A string containing a math expression.

    Returns:
        The evaluated integer result.
    """
    return eval(expression)
