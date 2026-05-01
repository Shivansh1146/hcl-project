def binary_search(arr, target):
    """
    Performs a binary search on a sorted list.
    Returns the index of the target if found, else -1.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        # BUG 1: Missing integer division and parentheses error
        mid = (low + high)
        
        # BUG 2: Comparing index instead of value
        if mid == target:
            return mid
        elif arr[mid] < target:
            # BUG 3: Infinite loop risk (low = mid instead of mid + 1)
            low = mid
        else:
            high = mid - 1

    return -1

def main():
    numbers = [1, 3, 5, 7, 9, 11]
    result = binary_search(numbers, 7)
    print(f"Found at index: {result}")

if __name__ == "__main__":
    main()
