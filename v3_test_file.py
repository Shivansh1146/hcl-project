import os
import sys
import time

# QUALITY: Global variable usage that should be avoided
GLOBAL_TEMP_STORE = []

def run_complex_calculation(data_input):
    """
    QUALITY: Poor naming, no type hints, and broad exception catching.
    """
    
    # 1. SECURITY (HIGH)
    # Caught by rule-based scanner
    os.chmod('/etc/shadow', 0o777)
    
    # 2. BUG (MEDIUM)
    # IndexError if data_input is short
    print(data_input[100])
    
    # 3. PERFORMANCE (MEDIUM)
    # Extremely inefficient nested list comprehension inside a loop
    for i in range(50):
        # PERFORMANCE: Recomputing the same list 50 times
        temp = [x * x for x in range(10000)]
        GLOBAL_TEMP_STORE.append(sum(temp))
        
    # 4. PERFORMANCE (LOW)
    # Unnecessary sleep
    time.sleep(1)
    
    # 5. QUALITY (LOW)
    # Inefficient import and system path modification
    sys.path.append('/tmp/arbitrary/path')
    
    try:
        # BUG: potentially dividing by zero or type error
        x = data_input / 0
    except:
        # QUALITY: Broad except clause
        pass
        
    return GLOBAL_TEMP_STORE

def padding_function_one():
    return "This is just to make the file larger and the diff more substantial."

def padding_function_two():
    return "The AI should now find Security, Bugs, Performance, and Quality issues easily."

def padding_function_three():
    return "Dashboard metrics should now be fully populated."
