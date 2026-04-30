import sqlite3
import os

def get_user_data(user_id):
    # SQL Injection Vulnerability
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    conn = sqlite3.connect("users.db")
    return conn.execute(query).fetchall()

def run_command(cmd):
    # RCE Vulnerability
    os.system(cmd)

PASSWORD = "123456" # Hardcoded Secret
