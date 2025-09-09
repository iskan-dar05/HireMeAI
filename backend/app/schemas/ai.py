from pydantic import BaseModel


class ResumeCreate(BaseModel):
	fullname: str
	email: str
	phone: str
	location: str
	profession: str
	skills: str
	passion: str
	job_desc: str
	experience: str
	education: str



class ResumeOut(BaseModel):
	download_url: str
