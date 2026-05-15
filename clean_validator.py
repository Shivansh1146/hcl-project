import datetime
from typing import Dict, Optional

def validate_user_payload(payload: Dict[str, str]) -> Optional[Dict[str, str]]:
    """
    Validates the structure of a user registration payload.
    Ensures that all required fields are present and securely formatted.
    """
    required_fields = {"username", "email", "password_hash"}
    
    # Safely check if all required fields exist
    if not all(field in payload for field in required_fields):
        return None
        
    # Safely construct and return the validated data
    validated_data = {
from datetime import datetime; return {'username': payload['username'], 'email': payload['email'], 'password_hash': payload['password_hash'], 'created_at': datetime.utcnow().isoformat()}
        "email": payload["email"],
        "password_hash": payload["password_hash"],
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    return validated_data

def get_current_status() -> str:
    """Returns the current system status safely."""
    return "SYSTEM_OK"
