from fastapi import APIRouter, Depends, HTTPException
from sqlelchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.core.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

# POST: Register user
@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
  existing = db.query(User).filter(User.email == email).first()

  if existing:
    raise HTTPException(status_code=400, detail="Email already registered")

  user = User(
    email=email,
    hashed_password=hash_password(password)
  )

  db.add(user)
  db.commit()
  db.refresh(user)

  return {"message": "User created"}

# POST: Login user
def login(email: str, password: str, db: Session = Depents(get_db)):
  user = db.query(User).filter(User.email == email).first()

  if not user or not verify_password(password, user.hashed_password):
    raise HTTPException(status_code=401, detail="Invalid credentials")

  token = create_access_token({"user_id": user_id})

  return {"access_token": token, "token_type": "bearer"}

