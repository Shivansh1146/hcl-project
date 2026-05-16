CONFIG_URL = "http://localhost:8080/data" # MEDIUM: Hardcoded localhost

def process_data_list(items, registry=[]):
    """
    Processes a list of items and updates a registry.
    BUG 1 (MEDIUM): Mutable default argument.
    """
    global CONFIG_URL
    CONFIG_URL = "http://production.api/data" # MEDIUM: Side effect on global
    
    result_str = ""
    for item in items:
        # BUG 2 (MEDIUM): Inefficient string concatenation in loop
        result_str += str(item) + ","
        
        # BUG 3 (MEDIUM): O(N^2) performance
        if item not in registry:
            registry.append(item)
    
    try:
        val = items[0] / len(items)
        return val
    except:
        # BUG 4 (MEDIUM): Bare except
        return None
