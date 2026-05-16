import os

# MEDIUM 1: Global variable modified in function (side effect)
_cache = {}

def process_data_items(data, items=[]):
    """
    Processes items with multiple quality concerns.
    MEDIUM 2: Mutable default argument 'items=[]'.
    """
    global _cache
    _cache = {"last_data": data} # Side effect on global
    
    # MEDIUM 3: Inefficient O(N^2) search
    for x in data:
        if x in data:
            print(f"Item found: {x}")
            
    # MEDIUM 4: Bare except (PEP 8 violation)
    try:
        return data[0] if data else None
    except:
        return None

# MEDIUM 5: Hardcoded local development path
LOCAL_TEMP_PATH = "/Users/shivansh/Desktop/temp" # Hardcoded path
