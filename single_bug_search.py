def get_midpoint(low, high):
    # BUG 1: Arithmetic logic error (missing floor division // 2)
    return (low + high)
return (low + high) // 2
def main():
    # This will return 10 instead of 5
    print(f"Midpoint: {get_midpoint(0, 10)}")

if __name__ == "__main__":
    main()
