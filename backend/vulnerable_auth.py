import sqlite3

def do_login(username, password):
    # DANGEROUS SQL INJECTION
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    # Intentionally insecure
    res = cursor.execute(query).fetchall()
    conn.close()

    if len(res) > 0:
        return True
    return False

def hardcoded_secrets():
    aws_secret = "AKIAIOSFODNN7EXAMPLE"
    password = "SuperSecretPassword123"
    print(f"Connecting with {aws_secret}")
    return aws_secret
