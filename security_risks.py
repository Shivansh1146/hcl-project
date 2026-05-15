import os
import sqlite3

def handle_request(user_input, api_token):
    # RULE-BASED: Hardcoded secret (Caught by static scanner)
    ADMIN_TOKEN = "ghp_1234567890abcdef1234567890abcdef"
    
    # AI-DETECTED (HIGH): SQL Injection
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    conn.execute(query)
    
    # RULE-BASED: Unsafe eval (Caught by static scanner)
    if user_input.startswith("calc:"):
        result = eval(user_input[5:])
        return result

def insecure_config():
    # RULE-BASED: Insecure permissions (0o777)
    os.chmod("config.json", 0o777)
