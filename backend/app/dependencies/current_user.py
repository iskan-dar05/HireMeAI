from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_claims
from app.models.user import User

def get_current_user(claims: dict = Depends(get_claims), db: Session = Depends(get_db)) -> User:
    clerk_id = claims.get("sub")
    if not clerk_id:
        raise HTTPException(status_code=401, detail="Token subject missing")
    user = db.query(User).filter(User.clerk_user_id == clerk_id).one_or_none()
    if user is None:
        # Clerk user profile fields are not always present in session JWT claims.
        # Use a separate Clerk webhook/profile sync for email and name if needed.
        user = User(clerk_user_id=clerk_id, email=claims.get("email"), full_name=claims.get("name"))
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
