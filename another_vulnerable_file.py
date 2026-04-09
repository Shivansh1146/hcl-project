import subprocess
import yaml

def unsafe_cmd(user_dir):
    # CRITICAL: Command Injection
    return subprocess.getoutput("ls -la " + user_dir)

def parse_config(yaml_string):
    # CRITICAL: Insecure YAML Unserialization
    return yaml.load(yaml_string)

def print_password():
    # CRITICAL: Hardcoded Secret
    super_secret = "AKIA-FAKE-AWS-KEY-55555"
    print(super_secret)
