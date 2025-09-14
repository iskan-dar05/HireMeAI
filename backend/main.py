from fastapi import FastAPI
from app.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.resume import router as resume_router

app = FastAPI(title="HireMeAI API")

origins = [
	"http://localhost:8080",
	"http://127.0.0.1:8080"
]


app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)


# include auth routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(resume_router, prefix="/resume", tags=["Resume"])


@app.get("/")
def root():
	return {"message": "API is running"}


