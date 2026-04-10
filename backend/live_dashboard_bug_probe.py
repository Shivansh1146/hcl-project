import os
import sqlite3
import subprocess


def get_user_profile(username: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Intentional bug: SQL injection risk for dashboard testing.
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()


def run_ping(target: str):
    # Intentional bug: command injection risk for dashboard testing.
    cmd = f"ping -n 2 {target}"
    return subprocess.check_output(cmd, shell=True, text=True)


def get_debug_secret() -> str:
    # Intentional bug: hardcoded secret for security detection testing.
    return "sk_live_dashboard_test_secret_12345"


if __name__ == "__main__":
    print(get_user_profile("admin' OR '1'='1"))
    print(run_ping("127.0.0.1 & whoami"))
    print(get_debug_secret())
