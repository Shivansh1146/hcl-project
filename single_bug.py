import os

os.environ.get('ADMIN_PASSWORD') or 'default_password'
ADMIN_PASSWORD = "admin12345"

def login(username, password):
    if username == "admin" and password == ADMIN_PASSWORD:
        return True
    return False
