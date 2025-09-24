import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { api } from "@/services/axios"

const ResumeViewer = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const pdfUrl = queryParams.get("url");

  const [pdfBlobUrl, setPdfBlobUrl] = useState<string | null>(null);

  useEffect(()=>{
    if(pdfUrl){
	const fetchPdf = async () => {
	   try {
		const res = await api.get(pdfUrl, {responseType: "blob"})
		const blob = new Blob([res.data], {type: "application/pdf"})
		const url = URL.createObjectUrl(blob)
		setPdfBlobUrl(url)
	   } catch(err){
		console.error("Failed to load PDF:", err)
	   }
	}
	fetchPdf();
	}
  }, [pdfUrl])
   if (!pdfUrl) {
    return <p className="text-center mt-10 text-red-500">No PDF to show</p>;
  }
  ChatGPT
You said:
from fastapi import APIRouter, Depends, HTTPException, Request from fastapi.responses import FileResponse from sqlalchemy.orm import Session from app.schemas.ai import ResumeCreate, ResumeOut from services.create_resume import generate_resume from app.utils.pdf_export import save_to_pdf from app.models.user import User from app.core.security import get_current_user import os      router = APIRouter()  @router.post("/create-resume", response_model=ResumeOut) def create_resume(resume_info: ResumeCreate, request: Request, current_user: User = Depends(get_current_user)): 	user_info = { 		"fullname": resume_info.fullname, 		"email": resume_info.email, 		"phone": resume_info.phone, 		"location": resume_info.location, 		"profession": resume_info.profession, 		"skills": resume_info.skills, 		"passion": resume_info.passion, 		"job_desc": resume_info.job_desc, 		"experience": resume_info.experience, 		"education": resume_info.education 	}  	job_desc = resume_info.job_desc  	resume_text = generate_resume(job_desc, user_info) 	pdf_path = save_to_pdf(resume_text)  	base_url = str(request.base_url).rstrip("/") 	download_url = f"{base_url}/resume/download-resume?file={pdf_path}" 	view_url = f"{base_url}/resume/view-resume?file={pdf_path}"  	return { 		"download_url": download_url, 		"view_url": view_url 		}   @router.get("/view-resume") def view_resume(file: str, current_user: User = Depends(get_current_user)): 	file_path = os.path.join("app", "outputs", file) 	if not os.path.exists(file_path): 		raise HTTPException(status_code=404, detail="File not found") 	return FileResponse(file_path, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={file}"}) 	  @router.get("/download-resume") def download_resume(file: str):     file_path = os.path.join("app", "outputs", file)  # <-- corrected path     print(file_path)     if not os.path.exists(file_path):         raise HTTPException(status_code=404, detail="File not found")      return FileResponse(file_path, media_type="application/pdf", filename=file)      import { api } from "./axios"


export interface FormData{
	fullname: string,
	email: string,
	phone: string,
	location: string,
	profession: string,
	passion: string,
	experience: string,
	job_desc: string,
	skills: string,
	education: string
}


export const createResume = async (data: FormData)=>{
	const res = await api.post("/resume/create-resume", data)
	return res.data
}




import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import Navbar from "@/components/Navbar";
import { useState } from "react";
import { createResume } from "@/services/resume"
import { useNavigate } from "react-router-dom"

const CreateResume = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    fullname: "",
    email: "",
    phone: "",
    location: "",
    profession: "",
    passion: "",
    experience: "",
    job_desc: "",
    skills: "",
    education: ""
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try{
      const res = await createResume(formData);
      console.log("Craeet CV success", res)
      alert("Create CV successful!");
      if(res.download_url)
      {
        navigate(/resume-viewer?url=${encodeURIComponent(res.view_url)});
      }
    }catch(err)
    {
      console.error(err);
      alert("Create CV Failed");
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <div className="container mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Create Your <span className="bg-gradient-primary bg-clip-text text-transparent">CV</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Fill in your details to generate a professional resume
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <Card className="shadow-elegant bg-gradient-card">
            <CardHeader>
              <CardTitle>Personal Information</CardTitle>
              <CardDescription>
                Tell us about yourself and what makes you unique
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="fullName">Full Name *</Label>
                  <Input 
                    id="fullName"
                    value={formData.fullname}
                    onChange={(e) => handleInputChange("fullname", e.target.value)}
                    placeholder="Enter your full name"
                    className="transition-all focus:shadow-glow"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address *</Label>
                  <Input 
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange("email", e.target.value)}
                    placeholder="your.email@example.com"
                    className="transition-all focus:shadow-glow"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="phone">Phone Number</Label>
                  <Input 
                    id="phone"
                    value={formData.phone}
                    onChange={(e) => handleInputChange("phone", e.target.value)}
                    placeholder="Your phone number"
                    className="transition-all focus:shadow-glow"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="location">Location</Label>
                  <Input 
                    id="location"
                    value={formData.location}
                    onChange={(e) => handleInputChange("location", e.target.value)}
                    placeholder="City, Country"
                    className="transition-all focus:shadow-glow"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="profession">Professional Title *</Label>
                <Input 
                  id="profession"
                  value={formData.profession}
                  onChange={(e) => handleInputChange("profession", e.target.value)}
                  placeholder="e.g., Frontend Developer, Marketing Manager"
                  className="transition-all focus:shadow-glow"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="whatILove">What I Love / Passion *</Label>
                <Textarea 
                  id="whatILove"
                  value={formData.passion}
                  onChange={(e) => handleInputChange("passion", e.target.value)}
                  placeholder="Tell us what you're passionate about in your career..."
                  className="min-h-[100px] transition-all focus:shadow-glow"
                />
              </div>

               <div className="space-y-2">
                <Label htmlFor="JobDesc">Job Description</Label>
                <Textarea 
                  id="JobDesc"
                  value={formData.job_desc}
                  onChange={(e) => handleInputChange("job_desc", e.target.value)}
                  placeholder="Job Description"
                  className="min-h-[100px] transition-all focus:shadow-glow"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="experience">Work Experience</Label>
                <Textarea 
                  id="experience"
                  value={formData.experience}
                  onChange={(e) => handleInputChange("experience", e.target.value)}
                  placeholder="Describe your work experience, previous roles, achievements..."
                  className="min-h-[120px] transition-all focus:shadow-glow"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="skills">Skills</Label>
                <Textarea 
                  id="skills"
                  value={formData.skills}
                  onChange={(e) => handleInputChange("skills", e.target.value)}
                  placeholder="List your key skills, technologies, languages..."
                  className="min-h-[100px] transition-all focus:shadow-glow"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="education">Education</Label>
                <Textarea 
                  id="education"
                  value={formData.education}
                  onChange={(e) => handleInputChange("education", e.target.value)}
                  placeholder="Your educational background, degrees, certifications..."
                  className="min-h-[100px] transition-all focus:shadow-glow"
                />
              </div>

              <div className="flex gap-4 pt-6">
                <Button 
                  variant="outline" 
                  className="flex-1 transition-all hover:shadow-card"
                >
                  Save Draft
                </Button>
                <Button 
                  className="flex-1 bg-gradient-primary hover:shadow-glow transition-all"
                >
                  Generate CV
                </Button>
              </div>
            </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default CreateResume; why when console is return just download_url no view_url
ChatGPT said:
Got it ✅ — I see the issue.

In your FastAPI backend, you’re returning both download_url and view_url:

return {
    "download_url": download_url,
    "view_url": view_url
}
So if your console only shows download_url and not view_url, it’s usually one of these problems:

1. Mismatch in Response Model (ResumeOut)
You’re using response_model=ResumeOut in:

@router.post("/create-resume", response_model=ResumeOut)
If your ResumeOut schema does not include view_url, FastAPI will filter it out.
👉 That’s why only download_url shows up in your response.

Example of the problem:

class ResumeOut(BaseModel):
    download_url: str   # <-- only this field exists
FastAPI automatically strips fields not defined in the response model.

✅ Fix: Add view_url to your schema:

class ResumeOut(BaseModel):
    download_url: str
    view_url: str
2. Frontend Handling
In your React code, you log:

console.log("Craeet CV success", res)
If view_url isn’t inside res, check the backend schema as above.

But if it is there in the raw API response but not in React, then maybe your Axios interceptor (in ./axios) or createResume function is modifying the response.

Quick check:

const res = await createResume(formData);
console.log("RAW response", res);
console.log("Only data", res.data);
Summary
If ResumeOut doesn’t have view_url → add it.

If it has, but still missing → check your Axios wrapper.

👉 Do you want me to adjust your ResumeOut schema properly so it supports both URLs?

You said:
give me job description for fuulstack dev to test in my project
ChatGPT said:
Here’s a sample job description for a Full-Stack Developer you can use to test your resume generator project:

Job Title: Full-Stack Developer

Job Description:
We are seeking a talented Full-Stack Developer to join our growing team. The ideal candidate will be responsible for building scalable web applications, integrating APIs, and ensuring smooth performance across both frontend and backend systems.

Responsibilities:

Design, develop, and maintain web applications using modern frameworks.

Build and manage RESTful APIs and database models.

Collaborate with designers and product managers to deliver user-friendly features.

Optimize applications for maximum performance and scalability.

Write clean, maintainable, and efficient code.

Implement authentication, security, and data protection best practices.

Troubleshoot, debug, and upgrade existing systems.

Requirements:

Strong proficiency in JavaScript/TypeScript, HTML, CSS.

Experience with frontend frameworks such as React, Vue, or Angular.

Experience with backend frameworks like Node.js, Django, or FastAPI.

Knowledge of databases (MySQL, PostgreSQL, MongoDB).

Familiarity with REST APIs and GraphQL.

Understanding of cloud platforms (AWS, Azure, or GCP).

Experience with Git/GitHub and CI/CD pipelines.

Strong problem-solving and communication skills.

Nice to Have:

Experience with Docker and containerization.

Familiarity with testing frameworks (Jest, PyTest, Mocha).

Knowledge of DevOps practices.

Would you like me to also create a shorter version (2–3 sentences) that is optimized for your resume generator’s AI input? This way the test won’t be too long.

You said:
import { useLocation } from "react-router-dom"


const ResumeViewer = ()=>{
	const location = useLocation();
	const queryParams = new URLSearchParams(location.search);
	const pdfUrl = queryParams.get("url");

	if(!pdfUrl)
	{
		return <p className="text-center mt-10 text-red-500">No PDF to show</p>;
	}

	return (
		<div className="flex flex-col items-center p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Your Generated Resume</h1>

      <div className="w-full max-w-4xl bg-white shadow-lg rounded-lg overflow-hidden">
        <iframe
          src={pdfUrl}
          title="Resume PDF"
          className="w-full h-[80vh]"
        ></iframe>
      </div>

      <a
        href={pdfUrl}
        download="resume.pdf"
        className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
      >
        Download PDF
      </a>
    </div>
	)
}

export default ResumeViewer
 how i use token to get this url pdf because i make view_pdf route should auth
ChatGPT said:
Great question 👍 You’re right — since your /resume/view-resume route is protected by authentication, your React app must include the JWT token when requesting the PDF.

🔹 Why your current code fails
Right now your <iframe src={pdfUrl} /> just hits the URL directly. That means no Authorization: Bearer <token> header is sent → FastAPI rejects it.

🔹 Options to Fix It
Option 1. Create a backend proxy route (best UX)
Instead of giving the frontend the direct PDF path, you create an authenticated endpoint that streams the PDF.

The frontend calls your API with Axios (including the token).

Your API returns the PDF file blob.

The frontend then creates an object URL to show it in <iframe>.

Example:

Backend (FastAPI) → keep /view-resume with auth:

@router.get("/view-resume")
def view_resume(file: str, current_user: User = Depends(get_current_user)):
    file_path = os.path.join("app", "outputs", file)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type="application/pdf")
Frontend (React) → fetch PDF with token and show:

import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { api } from "@/services/axios"; // your axios instance with token interceptor

const ResumeViewer = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const pdfUrl = queryParams.get("url");

  const [pdfBlobUrl, setPdfBlobUrl] = useState<string | null>(null);

  useEffect(() => {
    if (pdfUrl) {
      const fetchPdf = async () => {
        try {
          const res = await api.get(pdfUrl, { responseType: "blob" }); 
          const blob = new Blob([res.data], { type: "application/pdf" });
          const url = URL.createObjectURL(blob);
          setPdfBlobUrl(url);
        } catch (err) {
          console.error("Failed to load PDF:", err);
        }
      };
      fetchPdf();
    }
  }, [pdfUrl]);

  if (!pdfUrl) {
    return <p className="text-center mt-10 text-red-500">No PDF to show</p>;
  }

  return (
    <div className="flex flex-col items-center p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Your Generated Resume</h1>

      {pdfBlobUrl ? (
        <div className="w-full max-w-4xl bg-white shadow-lg rounded-lg overflow-hidden">
          <iframe src={pdfBlobUrl} title="Resume PDF" className="w-full h-[80vh]" />
        </div>
      ) : (
        <p>Loading PDF...</p>
      )}

      {pdfBlobUrl && (
        <a
          href={pdfBlobUrl}
          download="resume.pdf"
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
        >
          Download PDF
        </a>
      )}
    </div>
  );
}
