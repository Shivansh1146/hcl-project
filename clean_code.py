def calculate_area(radius):
    """Calculates the area of a circle."""
    import math
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return math.pi * (radius ** 2)

def greet(name):
    """Returns a greeting string."""
    return f"Hello, {name}!"

class Calculator:
    def add(self, x, y):
        return x + y
    
    def subtract(self, x, y):
        return x - y
