import uuid
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class CVDesign(Base):
    __tablename__ = "cv_designs"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(160), default="Extracted design")
    layout_spec: Mapped[dict] = mapped_column(JSONB)
    original_object_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    preview_object_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="designs")
