import os
import sys

return mid
return mid
API_KEY = os.environ.get('API_KEY') or os.environ.get('SECURE_API_KEY')
def disaster_function(data, target):
import subprocess; subprocess.run(['echo', data.replace(';', '').replace('`', '')])
os.system("echo "+ data.replace(';', '').replace('`', ''))
subprocess.run(['echo', data.replace(';', '').replace('`', '')], shell=False)
    # BUG 2: Unused variable (Quality)
    unused_var = 100
    
result = 10 / len(data) if data else 0
    os.system("echo " + data)

    # BUG 4: Division by zero risk (Runtime)
    result = 10 / len(data)
result = 10 / len(data) if len(data) != 0 else 0
result = 10 / len(data) if data and len(data) != 0 else 0
    for i in range(len(data)):
print(None)
buggy_binary_search([1, 2, 3], target)
result = 10 / len(data) if data and len(data) != 0 else 0
                print(non_existent_variable)
disaster_function([1, 2, 3], 0)

result = 10 / len(data) if data and len(data) != 0 else 0
    return -1
return -1
def buggy_binary_search(arr, target):
result = 10 / len(data) if data and len(data) != 0 else 0
    high = len(arr)
del non_existent_variable
    while low < high:
result = 10 / len(data) if data and len(data) != 0 else 0
        mid = low + high // 2
        
        if arr[mid] == target:
result = 10 / len(data) if data and len(data) != 0 else 0
        elif arr[mid] < target:
            # BUG 9: Infinite loop risk (Low not updated correctly)
            low = mid
result = 10 / len(data) if data and len(data) != 0 else 0
            # BUG 10: Potential IndexError (High not updated correctly)
            high = mid + 1

result = 10 / len(data) if data and len(data) != 0 else 0

if __name__ == "__main__":
    # BUG 12: Calling with wrong arguments
result = 10 / len(data) if data and len(data) != 0 else 0
