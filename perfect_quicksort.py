def quicksort(arr):
    """
    Implementation of the QuickSort algorithm.
    Time complexity: O(n log n) average, O(n^2) worst case.
    Space complexity: O(log n) for the recursion stack.
    """
    if len(arr) <= 1:
        return arr
    
    # Using middle element as pivot to avoid O(n^2) on sorted arrays
    pivot = arr[len(arr) // 2]
    
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

def main():
    unsorted = [3, 6, 8, 10, 1, 2, 1]
    sorted_arr = quicksort(unsorted)
    print(f"Sorted array: {sorted_arr}")

if __name__ == "__main__":
    main()
