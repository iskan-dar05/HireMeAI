from pydantic import BaseModel, Field, ConfigDict
from typing import Any

class CVCreate(BaseModel):
    title: str = Field(default="Untitled CV", max_length=200)
    content: dict[str, Any] = Field(default_factory=dict)
    job_description: str | None = None
    design_id: str | None = None

class CVUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    content: dict[str, Any] | None = None
    job_description: str | None = None
    design_id: str | None = None

class CVOut(BaseModel):
    id: str
    title: str
    status: str
    content: dict[str, Any]
    design_id: str | None
    created_at: Any
    updated_at: Any
    has_pdf: bool
    model_config = ConfigDict(from_attributes=True)

class GenerateCVRequest(BaseModel):
    title: str = Field(default="AI-generated CV", max_length=200)
    personal_info: dict[str, Any]
    experience: list[dict[str, Any]] = Field(default_factory=list)
    education: list[dict[str, Any]] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    projects: list[dict[str, Any]] = Field(default_factory=list)
    certifications: list[dict[str, Any]] = Field(default_factory=list)
    job_description: str = Field(min_length=20, max_length=20000)
    design_id: str | None = None

class TailorCVRequest(BaseModel):
    job_description: str = Field(min_length=20, max_length=20000)
