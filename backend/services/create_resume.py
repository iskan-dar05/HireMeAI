from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


def generate_resume(job_desc: str, user_info: dict):

	api_key = os.getenv("GROQ_API_KEY")
	
	if not api_key:
		raise ValueError("⚠️ GROQ_API_KEY not found in .env file")

	client = Groq(
		api_key=api_key
	)


	fullname = user_info["fullname"]
	email = user_info["email"]
	phone = user_info["phone"]
	location = user_info["location"]
	profession = user_info["profession"]
	skills = user_info["skills"]
	passion = user_info["passion"]
	experience = user_info["experience"]
	education = user_info["education"]

	chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": (
                "You are an expert resume writer. "
                "Your task is to create professional, tailored resumes "
                "that match the candidate’s profile with the given job description. "
                "Make the resume concise, ATS-friendly, and well-formatted."
            )
        },
        {
            "role": "user",
            "content": f"""
			Generate a professional resume for the following candidate:

			Name: {fullname}
			Email: {email}
			Phone Number: {phone}
			Location: {location}
			Professional Title: {profession}
			Skills: {skills}
			Passion: {passion}
			Work Experience: {experience}
			Education: {education}

			Job Description:
			{job_desc}
			"""
        }
    ],
    model="llama-3.3-70b-versatile",
	)
	return chat_completion.choices[0].message.content




