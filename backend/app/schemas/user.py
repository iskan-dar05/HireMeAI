from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
	firstname: str
	lastname: str
	email: EmailStr
	password: str


class UserOut(BaseModel):
	id: int
	firstname: str
	lastname: str
	email: EmailStr
	is_active: bool

	class Config:
		orm_mode: True

class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str





