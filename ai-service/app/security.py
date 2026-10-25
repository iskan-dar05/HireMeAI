import hmac
from fastapi import Header, HTTPException
from app.config import settings

def verify_internal_secret(x_internal_secret: str | None = Header(default=None)):
    expected = settings.internal_api_secret
    if not expected or expected == "change-me":
        raise HTTPException(status_code=503, detail="Internal service secret is not configured")
    if not x_internal_secret or not hmac.compare_digest(x_internal_secret, expected):
        raise HTTPException(status_code=401, detail="Unauthorized internal service request")
