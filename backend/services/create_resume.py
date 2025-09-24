from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()



def generate_resume(job_desc: str, user_info: dict):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("⚠️ GROQ_API_KEY not found in .env file")

    client = Groq(api_key=api_key)

    prompt_template = f"""
    You are an expert resume writer. 
    Create a resume that is concise, ATS-friendly, and professional.
    Format it clearly with sections like SUMMARY, SKILLS, EXPERIENCE, and EDUCATION. 
    Align the resume with the given job description.

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

    Output:
    --------
    A structured resume text in the following format:

    [FULL NAME]  
    [PROFESSIONAL TITLE]  
    📧 [EMAIL] | 📞 [PHONE] | 📍 [LOCATION]  

    **Professional Summary**  
    - Tailored 2–3 sentence summary highlighting strengths and alignment with job description.

    **Skills**  
    - Skill 1  
    - Skill 2  
    - Skill 3  

    **Experience**  
    [Job Title] – [Company], [Years]  
    - Achievement 1  
    - Achievement 2  

    **Education**  
    [Degree] – [Institution], [Year]
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert resume writer."},
            {"role": "user", "content": prompt_template},
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.get("content", "").strip()
