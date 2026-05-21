from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import bcrypt
import os

load_dotenv()

access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
secret_key = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash password using bcrypt
def hash_password(password: str) -> str:
  return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# check if entered password's hash is the same as the one stored
def verify_password(plain_password: str, hashed_password: str) -> bool:
  return bcrypt.checkpw(
    plain_password.encode("utf-8"),
    hashed_password.encode("utf-8")
  )

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)

  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, secret_key, algorithm=algo)