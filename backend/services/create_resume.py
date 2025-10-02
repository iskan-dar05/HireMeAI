from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

def generate_resume(job_desc: str, user_info: dict):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("⚠️ GROQ_API_KEY not found in .env file")

    client = Groq(api_key=api_key)

    prompt_template = f"""
    You are an expert resume writer. 
    Your task is to create a professional, ATS-friendly, and concise resume.
    The resume should be aligned with the given job description **but never copy-paste from it**.
    Instead, rephrase and generalize requirements so the resume sounds original and tailored.

    Instructions:
    -------------
    1. Use the candidate information as the primary source.
    2. If the job description mentions a skill, tool, or requirement missing from the candidate data, 
       intelligently incorporate it into the resume (but in your own words, not exactly as written).
    3. Do not copy sentences from the job description. 
       Instead, generate natural wording that reflects the candidate's fit.
    4. Make the resume realistic (don’t invent degrees or jobs), 
       but you can expand on responsibilities, achievements, and skills to strengthen the profile.
    5. Keep formatting clean and ATS-friendly, with clear sections.
    6. Expand short skills like "Python" into "Experienced in Python for backend APIs, 
       data processing, and automation."  

    Output requirement:
    -------------------
    ⚠️ VERY IMPORTANT: Return the resume as a **valid JSON object ONLY**.
    - Do not include markdown fences (like ```json).
    - Do not add explanations or commentary.
    - Follow this exact schema:

    {{
      "fullname": "string",
      "email": "string",
      "phone": "string",
      "location": "string",
      "profession": "string",
      "skills": ["string", "string"],
      "experience": [
        {{"title": "string", "company": "string", "description": "string", "dates": "string"}}
      ],
      "education": [
        {{"school": "string", "degree": "string", "field": "string", "gpa": "string", "dates": "string"}}
      ],
      "passion": "string"
    }}

    Candidate Information:
    ----------------------
    Name: {user_info.get("fullname")}
    Email: {user_info.get("email")}
    Phone: {user_info.get("phone")}
    Location: {user_info.get("location")}
    Professional Title: {user_info.get("profession")}
    Skills: {user_info.get("skills")}
    Passion: {user_info.get("passion")}

    Work Experience:
    ----------------
    {user_info.get("experience")}

    Education:
    ----------
    {user_info.get("education")}

    Job Description:
    ----------------
    {job_desc}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert resume writer."},
            {"role": "user", "content": prompt_template},
        ],
        model="llama-3.3-70b-versatile",
    )

    raw_response = chat_completion.choices[0].message.content.strip()

    # Cleanup in case Groq adds ```json fences
    if raw_response.startswith("```"):
        raw_response = raw_response.strip("`").replace("json", "", 1).strip()

    # Try parsing JSON
    try:
        resume_json = json.loads(raw_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"⚠️ Groq did not return valid JSON.\nResponse:\n{raw_response}") from e

    return resume_json
