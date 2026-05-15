import os

def run_system_processes(user_id, data_list):
    """
    Simulates a kitchen sink of errors for testing.
    """
    # 1. SECURITY (High Severity) - Caught by Rule-Based Scanner
    os.chmod('/tmp/system_logs', 0o777)
    
    # 2. BUG (Medium Severity)
    # The AI should suggest a fix to avoid KeyError, e.g.: val = data_dict.get(k)
    data_dict = {}
    for k in data_list:
        val = data_dict[k]
        print(val)
        
    # 3. PERFORMANCE (Low Severity)
    # The AI should suggest using str.join() instead of += in a loop
    # e.g.: combined = "".join(str(i) for i in range(1000))
    combined = ""
    for i in range(1000):
        combined += str(i)
        
    # 4. QUALITY (Low Severity)
    # The AI should suggest removing this unused variable
    # e.g.: remove the line completely
    unused_local_variable = 999
    
    return combined

class PaddingClassToBypassFilters:
    """This class pads the PR to be greater than 10 lines."""
    def __init__(self):
        self.pad1 = "pad1"
        self.pad2 = "pad2"
        self.pad3 = "pad3"
        self.pad4 = "pad4"
        self.pad5 = "pad5"
