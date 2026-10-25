from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/users", tags=["users"])

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=200)

@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": str(user.id), "clerk_user_id": user.clerk_user_id, "email": user.email,
            "full_name": user.full_name, "created_at": user.created_at}

@router.patch("/me")
def update_me(payload: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.full_name is not None:
        user.full_name = payload.full_name
    db.commit()
    db.refresh(user)
    return {"id": str(user.id), "email": user.email, "full_name": user.full_name}

@router.delete("/me", status_code=202)
def delete_me():
    raise HTTPException(status_code=501, detail="Account deletion requires a background cleanup workflow; not enabled in this starter.")
