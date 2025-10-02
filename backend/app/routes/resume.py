from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.schemas.ai import ResumeCreate, ResumeOut
from services.create_resume import generate_resume
from app.utils.pdf_export import save_to_pdf
from app.models.user import User
import tempfile
from app.core.security import get_current_user
import os

from app.core.templates import templates





router = APIRouter()

@router.post("/create-resume")
async def create_resume(
    request: Request,
    current_user: User = Depends(get_current_user),
	fullname: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    location: str = Form(None),
    profession: str = Form(...),
    passion: str = Form(...),
    job_desc: str = Form(None),
    skills: str = Form(None),
    experience: str = Form(None),  # could send JSON string and parse it
    education: str = Form(None),   # same here
    image: UploadFile = File(None)

    ):

    tmp_path = None

    if image:
        contents = await image.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

    user_info = {
        "fullname": fullname,
        "email": email,
        "phone": phone,
        "location": location,
        "profession": profession,
        "image": image,
        "skills": skills,
        "passion": passion,
        "experience": experience,
        "education": education,
        "image": tmp_path
    }

    job_desc = job_desc

    resume_text = generate_resume(job_desc, user_info)
    if hasattr(resume_text, "content"):
        resume_text = resume_text.content
    # pdf_path = save_to_pdf(resume_text)

    # base_url = str(request.base_url).rstrip("/")
    # download_url = f"{base_url}/resume/download-resume?file={pdf_path}"
    # view_url = f"{base_url}/resume/view-resume?file={pdf_path}"

    # return {
	# 	"download_url": download_url,
	# 	"view_url": view_url
	# 	}
    return templates.TemplateResponse(
        "index.html", {"request": request, "user_info": resume_text}
    )

    # return {"resume_text": resume_text}

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









