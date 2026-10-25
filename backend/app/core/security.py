import time
import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import settings

bearer = HTTPBearer(auto_error=False)
_jwks_client = None
_jwks_url_cached = None

def verify_clerk_token(token: str) -> dict:
    global _jwks_client, _jwks_url_cached
    if not settings.clerk_jwks_url or not settings.clerk_issuer:
        raise HTTPException(status_code=503, detail="Clerk JWT verification is not configured")
    try:
        if _jwks_client is None or _jwks_url_cached != settings.clerk_jwks_url:
            _jwks_client = PyJWKClient(settings.clerk_jwks_url, cache_keys=True)
            _jwks_url_cached = settings.clerk_jwks_url
        signing_key = _jwks_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256"],
            issuer=settings.clerk_issuer,
            options={"require": ["exp", "iat", "sub"]},
            leeway=30,
        )
        azp = claims.get("azp")
        if settings.authorized_parties and azp and azp not in settings.authorized_parties:
            raise HTTPException(status_code=401, detail="Invalid authorized party")
        if settings.authorized_parties and not azp:
            # Some Clerk token configurations omit azp; configure claims consistently for your app.
            raise HTTPException(status_code=401, detail="Missing authorized party claim")
        return claims
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired Clerk session token")

def get_claims(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    return verify_clerk_token(credentials.credentials)
