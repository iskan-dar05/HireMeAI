from pydantic import BaseModel





class ResumeCreate(BaseModel):
    fullname: str
    email: str
    phone: str
    location: str
    profession: str
    image: str | None = None
    skills: str       # 👈 plain string (multi-line)
    passion: str
    job_desc: str
    experience: str   # 👈 plain string (multi-line)
    education: str    # 👈 plain string (multi-line)


class ResumeOut(BaseModel):
	# download_url: str
	# view_url: str
    resume_text: str
