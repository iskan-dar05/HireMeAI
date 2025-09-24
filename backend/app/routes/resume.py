from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.schemas.ai import ResumeCreate, ResumeOut
from services.create_resume import generate_resume
from app.utils.pdf_export import save_to_pdf
from app.models.user import User
from app.core.security import get_current_user
import os





router = APIRouter()

@router.post("/create-resume", response_model=ResumeOut)
def create_resume(resume_info: ResumeCreate, request: Request, current_user: User = Depends(get_current_user)):
	user_info = {
        "fullname": resume_info.fullname,
        "email": resume_info.email,
        "phone": resume_info.phone,
        "location": resume_info.location,
        "profession": resume_info.profession,
        "image": resume_info.image,
        "skills": resume_info.skills,
        "passion": resume_info.passion,
        "job_desc": resume_info.job_desc,
        "experience": [exp.dict() for exp in resume_info.experience],
        "education": [edu.dict() for edu in resume_info.education],
    }

	job_desc = resume_info.job_desc

	resume_text = generate_resume(job_desc, user_info)
	pdf_path = save_to_pdf(resume_text)

	base_url = str(request.base_url).rstrip("/")
	download_url = f"{base_url}/resume/download-resume?file={pdf_path}"
	view_url = f"{base_url}/resume/view-resume?file={pdf_path}"

	return {
		"download_url": download_url,
		"view_url": view_url
		}


@router.get("/view-resume")
def view_resume(file: str, current_user: User = Depends(get_current_user)):
	file_path = os.path.join("app", "outputs", file)
	if not os.path.exists(file_path):
		raise HTTPException(status_code=404, detail="File not found")
	return FileResponse(file_path, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={file}"})
	

@router.get("/download-resume")
def download_resume(file: str):
    file_path = os.path.join("app", "outputs", file)  # <-- corrected path
    print(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type="application/pdf", filename=file)









