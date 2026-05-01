def buggy_quicksort(arr):
    # BUG 1: Missing base case (will cause recursion error on empty/tiny lists)
    # if len(arr) <= 1: return arr
    
    pivot = arr[0]
    
    # BUG 2: Logical error in partitioning (skips elements equal to pivot)
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]
    
    # BUG 3: Infinite recursion because pivot is not removed from partitions
    return buggy_quicksort(left) + [pivot] + buggy_quicksort(right)

def main():
    unsorted = [3, 6, 8, 10, 1, 2, 1]
    result = buggy_quicksort(unsorted)
    print(result)

if __name__ == "__main__":
    main()
