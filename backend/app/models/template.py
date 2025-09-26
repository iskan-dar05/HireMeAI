from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Template(Base):
	__tablename__ = "templates"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(200), nullable=False)
	path = Column(String, nullable=False)
	thumbnail = Column(String, nullable=False)
	is_active = Column(Boolean, default=True)


