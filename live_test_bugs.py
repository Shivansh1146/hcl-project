import sqlite3

def authenticate_user(username, password):
    # Rule-Based Bug: Hardcoded credential/secret
    api_key = "mock_secret_value_for_testing_123"
    
    # AI-Detected Bug (High): SQL Injection vulnerability
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # Unsafe query construction
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    
    return bool(user)

def execute_custom_command(cmd_string):
    # Rule-Based Bug: Unsafe eval
    return eval(cmd_string)
