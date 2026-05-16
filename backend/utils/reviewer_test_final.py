import requests

# ISSUE 1 (MEDIUM): Hardcoded local development URL
API_ENDPOINT = "http://127.0.0.1:5000/v1/internal"

def process_complex_data(items, results_cache=[]):
    """
    ISSUE 2 (MEDIUM): Mutable default argument 'results_cache=[]'.
    """
    global API_ENDPOINT
    # ISSUE 3 (MEDIUM): Unnecessary global state modification (side effect)
    API_ENDPOINT = "http://localhost:9000" 

    # ISSUE 4 (MEDIUM): Highly inefficient O(N^2) search for duplicates
    for i in range(len(items)):
        for j in range(len(items)):
            if items[i] == items[j] and i != j:
                print("Duplicate item detected in processing loop")

    try:
        # Some operation
        val = items[0] / len(items)
        return val
    except:
        # ISSUE 5 (MEDIUM): Bare except suppresses all potential errors (PEP 8)
        return None
