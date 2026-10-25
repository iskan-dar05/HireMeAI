import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.cv import CV, CVVersion
from app.models.cv_design import CVDesign
from app.models.user import User
from app.core.storage import delete_object, put_bytes
from app.services.pdf_service import render_cv_pdf

def owned_cv(db: Session, user: User, cv_id: uuid.UUID) -> CV:
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == user.id).one_or_none()
    if cv is None:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv

def owned_design(db: Session, user: User, design_id: uuid.UUID | None) -> CVDesign | None:
    if design_id is None:
        return None
    design = db.query(CVDesign).filter(CVDesign.id == design_id, CVDesign.user_id == user.id).one_or_none()
    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")
    return design

def save_version(db: Session, cv: CV):
    latest = max((v.version_number for v in cv.versions), default=0)
    db.add(CVVersion(cv_id=cv.id, version_number=latest + 1, content=cv.content or {}, pdf_object_key=cv.pdf_object_key))

def export_pdf(db: Session, cv: CV, user: User) -> str:
    design = owned_design(db, user, cv.design_id)
    pdf = render_cv_pdf(cv, design)
    key = f"users/{user.id}/cvs/{cv.id}/current.pdf"
    put_bytes(key, pdf, "application/pdf")
    cv.pdf_object_key = key
    cv.status = "completed"
    save_version(db, cv)
    db.commit()
    return key

def delete_cv_files(cv: CV):
    delete_object(cv.pdf_object_key)
    for version in cv.versions:
        if version.pdf_object_key and version.pdf_object_key != cv.pdf_object_key:
            delete_object(version.pdf_object_key)
