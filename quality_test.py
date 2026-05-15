import os,sys,time

# BUG: Dividing by zero
def BugFunction(a, b):
    return a / 0

# QUALITY: CamelCase function name, missing docstring, multiple statements
def myQualityTestFunction(x):
    y=x+1;z=y*2;print(z)
    return z

# PERFORMANCE: reading file in loop
def perf_test():
    for i in range(10):
        with open('quality_test.py', 'r') as f:
            print(f.read())

# QUALITY: Unused function with no docstring
def unused_func_no_doc():
    pass

# SECURITY: rule based
def sec_test():
    os.chmod('quality_test.py', 0o777)

# PADDING
def pad():
    print("padding 1")
    print("padding 2")
    print("padding 3")
    print("padding 4")
    print("padding 5")
    print("padding 6")
    print("padding 7")
    print("padding 8")
    print("padding 9")
    print("padding 10")
