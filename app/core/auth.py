from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
secret_key = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)

  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, secret_key, algorithm=algo)