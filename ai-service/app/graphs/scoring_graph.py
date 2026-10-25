import json
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.groq_client import get_groq

def score_cv(content: dict, job_description: str) -> dict:
    model = get_groq()
    prompt = """Compare this CV with the job description. Return JSON with:
{"score": integer 0-100, "matched_skills": [string], "missing_skills": [string],
 "strengths": [string], "suggestions": [string]}.
Do not claim the score is an objective hiring prediction.
CV:\n""" + json.dumps(content, ensure_ascii=False) + "\nJob description:\n" + job_description
    response = model.invoke([
        SystemMessage(content="You are a cautious CV reviewer. Output valid JSON only."),
        HumanMessage(content=prompt)
    ])
    text = response.content if isinstance(response.content, str) else json.dumps(response.content)
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    result = json.loads(text)
    score = result.get("score")
    if not isinstance(score, int) or not 0 <= score <= 100:
        raise ValueError("Invalid score response")
    return result
