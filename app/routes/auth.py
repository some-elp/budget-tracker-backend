from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.core.auth import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterRequest
from app.schemas.auth import LoginRequest
from app.core.deps import get_current_user


router = APIRouter(tags=["auth"])

# POST: Register user
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
  existing = db.query(User).filter(User.email == data.email).first()

  if existing:
    raise HTTPException(status_code=400, detail="Email already registered")

  user = User(
    email=data.email,
    hashed_password=hash_password(data.password)
  )

  db.add(user)
  db.commit()
  db.refresh(user)

  return {"message": "User created"}

# POST: Login user
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == data.email).first()

  if not user or not verify_password(data.password, user.hashed_password):
    raise HTTPException(status_code=401, detail="Invalid credentials")

  token = create_access_token({"user_id": user.id})

  return {"access_token": token, "token_type": "bearer"}

# GET: for testing protected routes.
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

