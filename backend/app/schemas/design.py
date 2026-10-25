from pydantic import BaseModel, Field
from typing import Any

class DesignUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=160)
    layout_spec: dict[str, Any] | None = None
