import os

def run_system_command():
    user_data = "rm -rf /" 
    # HIGH: Remote Code Execution / Command Injection
    os.system(user_data) 

def db_query(user_id):
    # HIGH: SQL Injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def hardcoded_secret():
    # HIGH: Hardcoded Credential (Rule-based scanner should also catch this)
    api_key = "sk-1234567890abcdef1234567890abcdef"
    return api_key
