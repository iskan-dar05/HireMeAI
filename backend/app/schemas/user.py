from pydantic import BaseMode, EmailStr


class UserCreate(BaseModel):
	email: EmailStr
	password: str


class UserOut(BaseModel):
	id: int
	email: EmailStr
	is_active: bool

	class Config:
		orm_mode: True

class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str
	token_type: str





