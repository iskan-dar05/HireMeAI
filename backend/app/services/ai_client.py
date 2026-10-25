import httpx
from fastapi import HTTPException
from app.core.config import settings

class AIClient:
    async def post(self, path: str, payload: dict) -> dict:
        headers = {"X-Internal-Secret": settings.internal_api_secret}
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=180, write=30, pool=10)) as client:
                response = await client.post(f"{settings.ai_service_url.rstrip('/')}{path}", json=payload, headers=headers)
                response.raise_for_status()
                try:
                    result = response.json()
                except ValueError as exc:
                    raise HTTPException(status_code=502, detail="AI service returned invalid JSON") from exc
                if not isinstance(result, dict):
                    raise HTTPException(status_code=502, detail="AI service returned an invalid response")
                return result
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=502, detail="AI service request failed") from exc
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail="AI service unavailable") from exc

ai_client = AIClient()
