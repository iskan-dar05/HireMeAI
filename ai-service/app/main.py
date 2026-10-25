from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.config import settings
from app.security import verify_internal_secret
from app.schemas import GenerateRequest, TailorRequest, ScoreRequest, ExtractDesignRequest
from app.graphs.cv_generation_graph import generate_cv
from app.graphs.tailor_graph import tailor_cv
from app.graphs.scoring_graph import score_cv
from app.models.vision_client import vision_client

app = FastAPI(title="HireMeAI AI Service", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-service"}

@app.post("/internal/generate", dependencies=[Depends(verify_internal_secret)])
def generate(payload: GenerateRequest):
    try:
        return generate_cv(payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=502, detail="CV content generation failed") from exc

@app.post("/internal/tailor", dependencies=[Depends(verify_internal_secret)])
def tailor(payload: TailorRequest):
    try:
        return tailor_cv(payload.content, payload.job_description)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="CV tailoring failed") from exc

@app.post("/internal/score", dependencies=[Depends(verify_internal_secret)])
def score(payload: ScoreRequest):
    try:
        return score_cv(payload.content, payload.job_description)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="CV scoring failed") from exc

@app.post("/internal/extract-design", dependencies=[Depends(verify_internal_secret)])
async def extract_design(payload: ExtractDesignRequest):
    try:
        spec = await vision_client.extract_layout(payload.image_base64, payload.mime_type)
        return {"layout_spec": spec}
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Vision model extraction failed; verify vision endpoint configuration") from exc
