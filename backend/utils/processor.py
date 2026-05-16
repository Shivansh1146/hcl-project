def process_data_list(items, registry=[]):
    """
    Processes a list of items and updates a registry.
    BUG 1 (MEDIUM): Mutable default argument 'registry=[]'.
    """
    for item in items:
        # BUG 2 (MEDIUM): O(N^2) performance - linear search in registry inside loop.
        if item not in registry:
            registry.append(item)
    
    try:
        # Some complex operation
        result = items[0] / len(items)
        return result
    except:
        # BUG 3 (MEDIUM): Bare except suppresses all errors.
        return None
