import uuid
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class CV(Base):
    __tablename__ = "cvs"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    design_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("cv_designs.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(200), default="Untitled CV")
    status: Mapped[str] = mapped_column(String(32), default="draft")
    content: Mapped[dict] = mapped_column(JSONB, default=dict)
    pdf_object_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    job_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="cvs")
    versions = relationship("CVVersion", back_populates="cv", cascade="all, delete-orphan", order_by="CVVersion.version_number")

class CVVersion(Base):
    __tablename__ = "cv_versions"
    __table_args__ = (UniqueConstraint("cv_id", "version_number", name="uq_cv_version_number"),)
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    cv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cvs.id", ondelete="CASCADE"), index=True)
    version_number: Mapped[int] = mapped_column(Integer)
    content: Mapped[dict] = mapped_column(JSONB)
    pdf_object_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    cv = relationship("CV", back_populates="versions")
