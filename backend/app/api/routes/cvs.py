import uuid
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.storage import delete_object, get_bytes
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.models.cv import CV, CVVersion
from app.models.cv_design import CVDesign
from app.schemas.cv import CVCreate, CVUpdate
from app.services.cv_service import owned_cv, owned_design, save_version, export_pdf, delete_cv_files

router = APIRouter(prefix="/api/v1/cvs", tags=["cvs"])

def serialize(cv: CV):
    return {"id": str(cv.id), "title": cv.title, "status": cv.status, "content": cv.content,
            "design_id": str(cv.design_id) if cv.design_id else None,
            "created_at": cv.created_at, "updated_at": cv.updated_at, "has_pdf": bool(cv.pdf_object_key)}

@router.post("", status_code=201)
def create_cv(payload: CVCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    design_uuid = uuid.UUID(payload.design_id) if payload.design_id else None
    owned_design(db, user, design_uuid)
    cv = CV(user_id=user.id, title=payload.title, content=payload.content,
            job_description=payload.job_description, design_id=design_uuid)
    db.add(cv); db.commit(); db.refresh(cv)
    return serialize(cv)

@router.get("")
def list_cvs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cvs = db.query(CV).filter(CV.user_id == user.id).order_by(CV.updated_at.desc()).all()
    return {"items": [serialize(cv) for cv in cvs], "total": len(cvs)}

@router.get("/{cv_id}")
def get_cv(cv_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return serialize(owned_cv(db, user, cv_id))

@router.patch("/{cv_id}")
def update_cv(cv_id: uuid.UUID, payload: CVUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cv = owned_cv(db, user, cv_id)
    data = payload.model_dump(exclude_unset=True)
    if "design_id" in data:
        cv.design_id = uuid.UUID(data["design_id"]) if data["design_id"] else None
        owned_design(db, user, cv.design_id)
    for field in ("title", "content", "job_description"):
        if field in data and data[field] is not None:
            setattr(cv, field, data[field])
    cv.status = "draft"
    db.commit(); db.refresh(cv)
    return serialize(cv)

@router.delete("/{cv_id}", status_code=204)
def delete_cv(cv_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cv = owned_cv(db, user, cv_id)
    delete_cv_files(cv)
    db.delete(cv); db.commit()
    return Response(status_code=204)

@router.get("/{cv_id}/versions")
def list_versions(cv_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cv = owned_cv(db, user, cv_id)
    return {"items": [{"id": str(v.id), "version_number": v.version_number, "created_at": v.created_at,
                       "has_pdf": bool(v.pdf_object_key)} for v in cv.versions]}

@router.post("/{cv_id}/versions/{version_id}/restore")
def restore_version(cv_id: uuid.UUID, version_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cv = owned_cv(db, user, cv_id)
    version = db.query(CVVersion).filter(CVVersion.id == version_id, CVVersion.cv_id == cv.id).one_or_none()
    if version is None:
        raise HTTPException(status_code=404, detail="Version not found")
    cv.content = version.content
    cv.status = "draft"
    db.commit(); db.refresh(cv)
    return serialize(cv)

@router.post("/{cv_id}/export")
def export_cv(cv_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cv = owned_cv(db, user, cv_id)
    key = export_pdf(db, cv, user)
    return Response(content=get_bytes(key), media_type="application/pdf", headers={
        "Content-Disposition": f'attachment; filename="cv-{cv.id}.pdf"',
        "Cache-Control": "private, no-store",
    })

@router.get("/{cv_id}/download")
def download_cv(cv_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cv = owned_cv(db, user, cv_id)
    if not cv.pdf_object_key:
        raise HTTPException(status_code=404, detail="No PDF has been generated yet")
    return Response(content=get_bytes(cv.pdf_object_key), media_type="application/pdf", headers={
        "Content-Disposition": f'attachment; filename="cv-{cv.id}.pdf"',
        "Cache-Control": "private, no-store",
    })
