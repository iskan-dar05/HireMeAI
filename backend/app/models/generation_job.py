import uuid
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class GenerationJob(Base):
    __tablename__ = "generation_jobs"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    cv_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("cvs.id", ondelete="SET NULL"), nullable=True, index=True)
    task_type: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(24), default="PENDING")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)
