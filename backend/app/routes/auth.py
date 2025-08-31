from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate , UserOut
from app.models.user import User
from app.core.security import get_password_hash




router = APIRouter()

@router.post("/auth/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
	# Check if user exists
	existing = db.query(User).filter(User.email == user_in.email).first()
	if existing:
		raise HTTPException(status_code=400, detail="Email already registred")

	# Hash password
	hashed_pw = get_password_hash(user_in.password)

	# Create user
	new_user = User(email=user_in.email, hashed_password=hashed_pw, is_active=False)
	db.add(new_user)
	db.commit()
	db.refresh(new_user)

	return new_user

@router.post("/auth/login", )







