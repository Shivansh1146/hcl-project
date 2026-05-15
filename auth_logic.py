def verify_user(token):
    # Rule-Based Bug: Hardcoded credential/secret
    internal_token = "mock_secret_value_for_testing_123"
    
    if token == internal_token:
        print("User verified!")
        return True
    return False

def check_admin(username):
    admins = ['admin1', 'admin2']
    # Poor practice: Using eval dynamically
    is_admin = eval(f"'{username}' in {admins}")
    return is_admin
