from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import health, users, cvs, cv_generation, cv_designs

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["Content-Disposition"],
)
app.include_router(health.router)
app.include_router(users.router)
app.include_router(cvs.router)
app.include_router(cv_generation.router)
app.include_router(cv_designs.router)

@app.get("/")
def root():
    return {"name": settings.app_name, "docs": "/docs"}
