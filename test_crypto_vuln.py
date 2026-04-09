import hashlib

def hash_user_password(password):
    # BUG: using weak MD5 hashing for passwords
    hasher = hashlib.md5()
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()

def execute_config(config_data):
    # BUG: eval on config data
    return eval(config_data)
