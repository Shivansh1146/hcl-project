import os
import sqlite3

# BUG 1: Hardcoded sensitive information (Should be caught by Rule Guard)
STRIPE_API_KEY = "sk_test_51Mz9jR2eZOTs4x6e8x8x8x8x8x8x8x8x"

def get_user_data(user_id):
    # BUG 2: SQL Injection vulnerability (Should be caught by AI)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()

def process_data(user_input):
    # BUG 3: Unsafe use of eval() (Should be caught by Rule Guard)
    result = eval(user_input)
    return result

def update_permissions(user_id, role):
    # BUG 4: Missing authentication check (Should be caught by AI)
    # Anyone can update any user's role
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET role = '{role}' WHERE id = {user_id}")
    conn.commit()
    print(f"User {user_id} updated to {role}")

def dangerous_upload(filename, content):
    # BUG 5: Arbitrary file write / Path traversal (Should be caught by AI)
    with open(f"/tmp/uploads/{filename}", "w") as f:
        f.write(content)
