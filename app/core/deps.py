from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
  token: str = Depends(oauth2_scheme),
  db: Session = Depends(get_db)
):
  try:
    payload = jwt.decode(token, secret_key, algorithms=[algo])
    user_id: int = payload.get("user_id")

    if user_id is None:
      raise HTTPException(status_code=401, detail="Invalid token")

  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid token")

  user = db.query(User).filter(User.id == user_id).first()

  if not user:
    raise HTTPException(status_code=401, detail="User not found")

  return user