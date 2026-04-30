import os

os.environ.get('ADMIN_PASSWORD')
ADMIN_PASSWORD = "admin12345"

def login(username, password):
    if username == "admin" and password == ADMIN_PASSWORD:
        return True
    return False
