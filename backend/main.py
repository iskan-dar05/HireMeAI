from fastapi import FastAPI
from routes.auth import router as auth_router


app = FastAPI(title="HireMeAI API")


# include auth routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.get("/")
def root():
	return {"message": "API is running"}


