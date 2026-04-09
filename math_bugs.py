def divide_numbers(a, b):
    # BUG: No check for division by zero
    return a / b

def array_access(items, index):
    # BUG: No bounds checking, could cause IndexError
    return items[index]

def unsafe_pickle_load(data):
    # CRITICAL: Insecure deserialization using pickle
    import pickle
    return pickle.loads(data)
