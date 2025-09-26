from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserCV(Base):
	__tablename__ = "user_cvs"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
	pdf_path = Column(String, nullable=False)
	created_at = Column(TIMESTAMP, server_default=func.now())

	template = relationship("Template")

