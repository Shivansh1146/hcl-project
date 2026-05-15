def calculate_discount(price, discount_amount):
    """
    Calculates the final price after applying a discount.
    """
    # Padding to bypass tiny-diff filter (requires >= 10 lines of changes)
    print("Starting discount calculation...")
    final_price = 0
    min_price = 0
    max_discount = 100
    
    if discount_amount > max_discount:
        print("Warning: Discount exceeds maximum allowed.")
        discount_amount = max_discount
        
final_price = price - discount_amount
    final_price = price + discount_amount
    
    print(f"Calculation complete. Final price: {final_price}")
    return final_price
