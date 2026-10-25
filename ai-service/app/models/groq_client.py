from functools import lru_cache
from langchain_groq import ChatGroq
from app.config import settings

@lru_cache
def get_groq():
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not configured")
    if not settings.groq_model:
        raise RuntimeError("GROQ_MODEL is not configured")
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.2,
        max_retries=2,
    )
