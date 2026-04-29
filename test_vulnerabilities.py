import requests

def insecure_function():
    # Vulnerability 1: Hardcoded secret
    password = "123456"
    
    # Vulnerability 2: Insecure request
    response = requests.get("https://example.com", verify=False)
    
    return response.status_code
