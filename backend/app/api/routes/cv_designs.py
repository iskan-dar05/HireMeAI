import uuid, io
from PIL import Image, UnidentifiedImageError
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.storage import put_bytes, presigned_get, delete_object
from app.dependencies.current_user import get_current_user
from app.models.user import User
from app.models.cv_design import CVDesign
from app.schemas.design import DesignUpdate
from app.services.ai_client import ai_client

router = APIRouter(prefix="/api/v1/cv-designs", tags=["CV designs"])
ALLOWED = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}

@router.post("/extract", status_code=201)
async def extract_design(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if file.content_type not in ALLOWED:
        raise HTTPException(status_code=415, detail="Upload a PNG, JPEG, or WebP image")
    data = await file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image exceeds upload size limit")
    try:
        image = Image.open(io.BytesIO(data))
        image.verify()
        image = Image.open(io.BytesIO(data))
        if image.width > 6000 or image.height > 6000 or image.width < 100 or image.height < 100:
            raise HTTPException(status_code=400, detail="Image dimensions are not supported")
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Invalid image file")
    try:
        result = await ai_client.post("/internal/extract-design", {
            "image_base64": __import__("base64").b64encode(data).decode("ascii"),
            "mime_type": file.content_type
        })
        spec = result.get("layout_spec")
        if not isinstance(spec, dict):
            raise HTTPException(status_code=502, detail="AI service returned invalid design")
        design_id = uuid.uuid4()
        key = f"users/{user.id}/designs/{design_id}/original.{ALLOWED[file.content_type]}"
        put_bytes(key, data, file.content_type)
        design = CVDesign(id=design_id, user_id=user.id, name="Extracted design", layout_spec=spec, original_object_key=key)
        db.add(design); db.commit(); db.refresh(design)
        return {"id": str(design.id), "name": design.name, "layout_spec": design.layout_spec}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Design extraction failed") from exc

@router.get("")
def list_designs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(CVDesign).filter(CVDesign.user_id == user.id).order_by(CVDesign.created_at.desc()).all()
    return {"items": [{"id": str(x.id), "name": x.name, "layout_spec": x.layout_spec, "created_at": x.created_at} for x in items]}

@router.get("/{design_id}")
def get_design(design_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    design = db.query(CVDesign).filter(CVDesign.id == design_id, CVDesign.user_id == user.id).one_or_none()
    if not design: raise HTTPException(status_code=404, detail="Design not found")
    return {"id": str(design.id), "name": design.name, "layout_spec": design.layout_spec, "created_at": design.created_at}

@router.patch("/{design_id}")
def update_design(design_id: uuid.UUID, payload: DesignUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    design = db.query(CVDesign).filter(CVDesign.id == design_id, CVDesign.user_id == user.id).one_or_none()
    if not design: raise HTTPException(status_code=404, detail="Design not found")
    if payload.name is not None: design.name = payload.name
    if payload.layout_spec is not None: design.layout_spec = payload.layout_spec
    db.commit(); db.refresh(design)
    return {"id": str(design.id), "name": design.name, "layout_spec": design.layout_spec}

@router.delete("/{design_id}", status_code=204)
def delete_design(design_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    design = db.query(CVDesign).filter(CVDesign.id == design_id, CVDesign.user_id == user.id).one_or_none()
    if not design: raise HTTPException(status_code=404, detail="Design not found")
    delete_object(design.original_object_key); delete_object(design.preview_object_key)
    db.delete(design); db.commit()
