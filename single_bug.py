import os

# The Single Bug: Hardcoded Admin Password
ADMIN_PASSWORD = "admin12345"

def login(username, password):
    if username == "admin" and password == ADMIN_PASSWORD:
        return True
    return False
