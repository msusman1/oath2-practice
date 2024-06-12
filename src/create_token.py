from jose import jwt
from datetime import datetime, timedelta
from src.setting import ALGORITHM,SECRET_KEY

def create_access_token(username: str, validation_time: timedelta) -> str:
    expiry_minutes = datetime.utcnow() + validation_time
    json_data = {"sub": username, "exp": expiry_minutes}
    encoded_jwt = jwt.encode(json_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
  