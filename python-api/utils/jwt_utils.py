from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

def decode_jwt(token: str):
  try:
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    return payload.get("userId")
  except JWTError:
    return None
