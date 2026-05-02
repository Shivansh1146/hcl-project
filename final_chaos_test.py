import os
import subprocess

# BUG 1: Security - Hardcoded Token
SECRET = os.environ.get('SECRET_TOKEN')

def chaos_function(input_data):
    # BUG 2: Security - Command Injection
    os.system("echo " + input_data)

    # BUG 3: Performance - O(2^N) Complexity
    def rec(n):
        if n < 2: return n
        return rec(n-1) + rec(n-2)
    
    for i in range(20):
        print(rec(i))

    # BUG 4: Logic - Infinite Loop
    count = 0
    while count < 10:
        if count == 7:
            # BUG 5: Increment skipped in this branch
            continue 
        count += 1

    # BUG 6: Runtime - Division by Zero risk
    val = 100 / (len(input_data) - 4)

    # BUG 7: Logic - Identity bug (is vs ==)
    if input_data is "test":
        print("Identity match")

    # BUG 8: Quality - Unused import
    import datetime

    # BUG 9: Security - Potential Eval injection
    eval(input_data)

    # BUG 10: Runtime - Attribute Error
    return input_data.non_existent_method()

if __name__ == "__main__":
    chaos_function("test")
