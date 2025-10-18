import json
import os
from groq import Groq
from dotenv import load_dotenv
from app.utils.json_extract import merge_layout, simplify_layout

load_dotenv()


def extract_json_from_text(text: str) -> str:
    """Extract valid JSON portion from text (handles if model added explanations)."""
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        return text[start:end + 1]
    raise ValueError("⚠️ No JSON object found in model response.")


def generate_resume(job_desc: str, user_info: dict, path: str):
    """Send layout + job data to Groq and return updated layout with new text."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("⚠️ GROQ_API_KEY not found in .env file")

    client = Groq(api_key=api_key)

    simplified = simplify_layout(path)


    prompt = f"""
You are an expert resume editor.
You must respond ONLY with valid JSON (no commentary, no markdown).

You are given:
1. Candidate info (may be incomplete).
2. A job description.
3. The simplified JSON layout of a resume (with text, fonts, and positions).

Your job:
- Improve the text based on the job description and candidate info.
- Keep the exact same structure, same pages, and same text_blocks.
- Modify only the "text" fields.
- Do not remove or add blocks.

Return only JSON with this format:
{{
  "pages": [
    {{
      "page_number": 1,
      "text_blocks": [
        {{"index": 0, "text": "Improved text", "font": "Helvetica", "size": 12, "color": 0, "bbox": [0,0,0,0]}},
        ...
      ]
    }}
  ]
}}

Candidate Info:
{json.dumps(user_info, indent=2)}

Job Description:
{job_desc}

Current Resume Layout (simplified):
{json.dumps(simplified, indent=2)}
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a precise JSON generator. Output only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        model="llama-3.3-70b-versatile",
    )

    raw_response = chat_completion.choices[0].message.content.strip()

    # Clean up common wrappers
    if raw_response.startswith("```"):
        raw_response = raw_response.strip("`").replace("json", "", 1).strip()

    # Extract JSON from text if model adds explanations
    try:
        cleaned_json = extract_json_from_text(raw_response)
        new_layout_simplified = json.loads(cleaned_json)
    except Exception as e:
        raise ValueError(f"⚠️ Could not extract valid JSON from model:\n{raw_response}") from e

    # Merge new text into original layout
    with open('path', 'w', encoding="utf-8") as f:
        updated_layout = merge_layout(json.load(f), new_layout_simplified)

    # Optional: Save the updated layout
    with open("layout_updated.json", "w", encoding="utf-8") as f:
        json.dump(updated_layout, f, indent=2, ensure_ascii=False)

    print("✅ Resume layout updated successfully.")
    return updated_layout
