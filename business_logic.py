def process_order(cart):
    """Calculates total price for a shopping cart."""
    total = 0
    for item in cart:
        total += item['price'] * item['quantity']
    return total

def validate_email(email):
    """Simple email validation."""
    import re
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

class OrderManager:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)
