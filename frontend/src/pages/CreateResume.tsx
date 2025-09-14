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
        navigate(`/resume-viewer?url=${encodeURIComponent(res.view_url)}`);
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

export default CreateResume;