import httpx
import json
from app.config import settings
from langsmith import traceable


class VisionClient:
    """OpenAI-compatible hosted vision endpoint adapter for Groq."""
    
    @traceable(name="Analyze CV Design")
    async def extract_layout(self, image_base64: str, mime_type: str) -> dict:
        if settings.vision_provider != "hosted":
            raise RuntimeError("Only the hosted OpenAI-compatible provider is implemented.")
        if not settings.vision_api_base_url or not settings.vision_api_key:
            raise RuntimeError("Configure VISION_API_BASE_URL and VISION_API_KEY")
            
        endpoint = settings.vision_api_base_url.rstrip("/")
        if not endpoint.endswith("/chat/completions"):
            endpoint += "/chat/completions"
            
        prompt = """Analyze this CV/resume design image. Ignore and do not reproduce the person's private data.
Return ONLY JSON with this shape:
{
 "page":{"size":"A4","orientation":"portrait","margin_mm":12},
 "layout":{"columns":2,"sidebar":{"position":"left","width_percent":32,"background":"#243447"},"main":{"background":"#FFFFFF"}},
 "style":{"font_family":"Arial","heading_color":"#243447","body_color":"#333333","accent_color":"#55716D"},
 "sections":[{"name":"contact","column":"sidebar","order":1},{"name":"skills","column":"sidebar","order":2},{"name":"experience","column":"main","order":1}],
 "notes":["brief uncertainty notes"]
}
Estimate only visual layout, colors, typography and section positions. Use hex colors. Do not include names, emails, phone numbers, or other personal content. Columns must be 1 or 2; width_percent must be between 20 and 45. If unsure, return reasonable estimates."""

        headers = {
            "Authorization": f"Bearer {settings.vision_api_key}", 
            "Content-Type": "application/json"
        }
        
        body = {
            "model": settings.vision_model,
            "temperature": 0,
            # تفعيل ميزة JSON Mode لضمان استجابة متوافقة مع الـ JSON المقترح
            "response_format": {"type": "json_object"}, 
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url", 
                        "image_url": {
                            # Groq تدعم الصور الممررة كـ Base64 عبر صيغة الـ Data URI القياسية
                            "url": f"data:{mime_type};base64,{image_base64}"
                        }
                    }
                ]
            }]
        }
        
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(endpoint, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()
            
        text = data["choices"][0]["message"]["content"]
        if isinstance(text, list):
            text = "".join(part.get("text", "") for part in text if isinstance(part, dict))
            
        text = text.strip()
        # بما أننا استخدمنا JSON Mode، لن تحتاج غالباً لتنظيف وسم الـ ``` ولكن السطور التالية تحميك احتياطاً
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            
        parsed = json.loads(text)
        return validate_layout(parsed)

# تظل دالة validate_layout و vision_client كما هي في كودك الأصلي دون تغيير


def validate_layout(spec: dict) -> dict:
    if not isinstance(spec, dict):
        raise ValueError("Layout must be an object")

    layout = spec.get("layout", {})
    if not isinstance(layout, dict):
        layout = {}
        spec["layout"] = layout

    columns = layout.get("columns", 1)
    if columns not in (1, 2):
        layout["columns"] = 1

    sidebar = layout.get("sidebar", {})
    if not isinstance(sidebar, dict):
        sidebar = {}
        layout["sidebar"] = sidebar

    if "width_percent" in sidebar:
        try:
            sidebar["width_percent"] = max(
                20, min(45, int(sidebar["width_percent"]))
            )
        except (TypeError, ValueError):
            sidebar["width_percent"] = 32

    style = spec.get("style", {})
    if not isinstance(style, dict):
        style = {}
        spec["style"] = style

    for key in ("heading_color", "body_color", "accent_color"):
        value = style.get(key)
        if value and (
            not isinstance(value, str)
            or not value.startswith("#")
            or len(value) not in (4, 7)
        ):
            style.pop(key, None)

    sections = spec.get("sections", [])
    if not isinstance(sections, list):
        spec["sections"] = []

    return spec


vision_client = VisionClient()