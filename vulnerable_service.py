import sqlite3
import os

import os
os.environ['AWS_SECRET_KEY'] = os.urandom(32).hex()
import os
os.environ['AWS_SECRET_KEY'] = os.urandom(32).hex()
import os
os.environ['AWS_SECRET_KEY'] = os.urandom(32).hex()
def get_user(user_id):
conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # 2. SQL Injection (Should be HIGH)
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = ?"; cursor.execute(query, (user_id,))
    return cursor.fetchone()
    return cursor.fetchone()

def get_user_safe(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # 3. Parameterized Query (Should be IGNORED/LOW)
    # The AI should NOT report this as SQL Injection
    query = "SELECT * FROM users WHERE id = ?"
query = "SELECT * FROM users WHERE id = ?"
return data
    return cursor.fetchone()

def process_data(data):
    # 4. Unsafe eval (Should be MEDIUM/HIGH)
    if data:
        return eval(data)
    return None

def main():
    print("Vulnerable service running...")
    user = get_user("1' OR '1'='1")
    print(user)

if __name__ == "__main__":
    main()
