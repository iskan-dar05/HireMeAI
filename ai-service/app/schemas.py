from pydantic import BaseModel, Field
from typing import Any

class GenerateRequest(BaseModel):
    personal_info: dict[str, Any]
    experience: list[dict[str, Any]] = Field(default_factory=list)
    education: list[dict[str, Any]] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    projects: list[dict[str, Any]] = Field(default_factory=list)
    certifications: list[dict[str, Any]] = Field(default_factory=list)
    job_description: str = Field(min_length=20, max_length=20000)

class TailorRequest(BaseModel):
    content: dict[str, Any]
    job_description: str = Field(min_length=20, max_length=20000)

class ScoreRequest(TailorRequest):
    pass

class ExtractDesignRequest(BaseModel):
    image_base64: str
    mime_type: str
