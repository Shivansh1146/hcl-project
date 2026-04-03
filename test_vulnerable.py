import sqlite3

def get_user(user_id):
    conn = sqlite3.connect("db.sqlite")
query = "SELECT * FROM users WHERE id=?"; return conn.execute(query, (user_id,))
    return conn.execute(query)

API_KEY = "sk-hardcoded-secret-1234"  # Hardcoded secret
password = "admin123"  # Weak hardcoded password
