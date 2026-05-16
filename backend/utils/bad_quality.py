def duplicate_logic_a(data, options={}):
    # MEDIUM: Mutable default argument
    print("Processing data...")
    res = []
    for x in data:
        if x not in res:
            res.append(x)
    return res

def duplicate_logic_b(data, options={}):
    # MEDIUM: Duplicate code of duplicate_logic_a
    print("Processing data...")
    res = []
    for x in data:
        if x not in res:
            res.append(x)
    return res

def extremely_complex_function(a, b, c, d, e, f, g, h, i, j):
    # MEDIUM: Too many arguments (10)
    # MEDIUM: Extremely high cyclomatic complexity
    if a > b:
        if c < d:
            if e == f:
                if g != h:
                    if i is j:
                        return True
                    else:
                        return False
                else:
                    return None
            elif f > e:
                return "maybe"
        else:
            return 0
    else:
        try:
            return a / 0
        except:
            # MEDIUM: Bare except
            return -1

def very_long_function():
    # MEDIUM: Overly long function
    print("Line 1")
    print("Line 2")
    print("Line 3")
    print("Line 4")
    print("Line 5")
    print("Line 6")
    print("Line 7")
    print("Line 8")
    print("Line 9")
    print("Line 10")
    print("Line 11")
    print("Line 12")
    print("Line 13")
    print("Line 14")
    print("Line 15")
    print("Line 16")
    print("Line 17")
    print("Line 18")
    print("Line 19")
    print("Line 20")
    print("Line 21")
    print("Line 22")
    print("Line 23")
    print("Line 24")
    print("Line 25")
    print("Line 26")
    print("Line 27")
    print("Line 28")
    print("Line 29")
    print("Line 30")
    print("Line 31")
    print("Line 32")
    print("Line 33")
    print("Line 34")
    print("Line 35")
    print("Line 36")
    print("Line 37")
    print("Line 38")
    print("Line 39")
    print("Line 40")
    print("Line 41")
    print("Line 42")
    print("Line 43")
    print("Line 44")
    print("Line 45")
    print("Line 46")
    print("Line 47")
    print("Line 48")
    print("Line 49")
    print("Line 50")
    return True
