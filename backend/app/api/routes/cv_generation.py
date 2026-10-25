import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.models.cv import CV
from app.models.cv_design import CVDesign
from app.models.generation_job import GenerationJob
from app.schemas.cv import GenerateCVRequest, TailorCVRequest
from app.services.ai_client import ai_client
from app.services.cv_service import owned_cv, owned_design, export_pdf

router = APIRouter(tags=["AI CV generation"])

@router.post("/api/v1/cv-generation/generate", status_code=201)
async def generate_cv(payload: GenerateCVRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    design_uuid = uuid.UUID(payload.design_id) if payload.design_id else None
    owned_design(db, user, design_uuid)
    job = GenerationJob(user_id=user.id, task_type="generate_cv", status="RUNNING")
    db.add(job); db.commit(); db.refresh(job)
    try:
        result = await ai_client.post("/internal/generate", payload.model_dump(exclude={"design_id"}))
        content = result.get("content")
        if not isinstance(content, dict):
            raise HTTPException(status_code=502, detail="AI service returned invalid CV content")
        cv = CV(user_id=user.id, title=payload.title, content=content,
                job_description=payload.job_description, design_id=design_uuid, status="draft")
        db.add(cv); db.flush()
        job.cv_id = cv.id
        key = export_pdf(db, cv, user)
        job.status = "COMPLETED"; job.completed_at = datetime.now(timezone.utc)
        db.commit()
        return {"job_id": str(job.id), "status": job.status, "cv": {"id": str(cv.id), "title": cv.title},
                "download_url": f"/api/v1/cvs/{cv.id}/download"}
    except Exception as exc:
        db.rollback()
        job = db.query(GenerationJob).filter(GenerationJob.id == job.id).one_or_none()
        if job:
            job.status = "FAILED"; job.error_message = str(exc)[:1000]
            job.completed_at = datetime.now(timezone.utc); db.commit()
        if isinstance(exc, HTTPException):
            raise
        raise HTTPException(status_code=502, detail="CV generation failed") from exc

@router.post("/api/v1/cvs/{cv_id}/tailor")
async def tailor_cv(cv_id: uuid.UUID, payload: TailorCVRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cv = owned_cv(db, user, cv_id)
    result = await ai_client.post("/internal/tailor", {"content": cv.content, "job_description": payload.job_description})
    content = result.get("content")
    if not isinstance(content, dict):
        raise HTTPException(status_code=502, detail="AI service returned invalid CV content")
    return {"cv_id": str(cv.id), "content": content, "job_description": payload.job_description}

@router.post("/api/v1/cvs/{cv_id}/score")
async def score_cv(cv_id: uuid.UUID, payload: TailorCVRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cv = owned_cv(db, user, cv_id)
    return await ai_client.post("/internal/score", {"content": cv.content, "job_description": payload.job_description})

@router.get("/api/v1/generation-jobs/{job_id}")
def get_job(job_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id, GenerationJob.user_id == user.id).one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Generation job not found")
    return {"id": str(job.id), "status": job.status, "task_type": job.task_type,
            "cv_id": str(job.cv_id) if job.cv_id else None, "error_message": job.error_message,
            "created_at": job.created_at, "completed_at": job.completed_at}
