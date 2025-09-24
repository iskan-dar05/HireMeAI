import Navbar from "@/components/Navbar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Eye, Download, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";

interface Resume {
  id: number;
  title: string;
  created_at: string;
  view_url: string;
  download_url: string;
}

const Dashboard = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);

  useEffect(() => {
    // TODO: Replace with real API call
    setResumes([
      {
        id: 1,
        title: "Frontend Developer CV",
        created_at: "2025-09-17",
        view_url: "/resume/view-resume?file=frontend.pdf",
        download_url: "/resume/download-resume?file=frontend.pdf",
      },
      {
        id: 2,
        title: "Full-Stack Developer CV",
        created_at: "2025-09-15",
        view_url: "/resume/view-resume?file=fullstack.pdf",
        download_url: "/resume/download-resume?file=fullstack.pdf",
      },
    ]);
  }, []);

  const handleDelete = (id: number) => {
    // TODO: API call to delete CV
    setResumes(prev => prev.filter(r => r.id !== id));
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="container mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold mb-8 text-center">
          My <span className="bg-gradient-primary bg-clip-text text-transparent">Resumes</span>
        </h1>

        {resumes.length === 0 ? (
          <p className="text-center text-muted-foreground">
            You haven’t created any CVs yet.
          </p>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resumes.map((resume) => (
              <Card
                key={resume.id}
                className="shadow-elegant bg-gradient-card flex flex-col justify-between"
              >
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-blue-600" />
                    {resume.title}
                  </CardTitle>
                  <p className="text-sm text-muted-foreground">
                    Created on {resume.created_at}
                  </p>
                </CardHeader>
                <CardContent className="flex gap-3 mt-4">
                  <Button
                    variant="outline"
                    size="sm"
                    asChild
                    className="flex-1 flex items-center gap-2"
                  >
                    <a href={resume.view_url} target="_blank" rel="noopener noreferrer">
                      <Eye className="w-4 h-4" />
                      View
                    </a>
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    asChild
                    className="flex-1 flex items-center gap-2"
                  >
                    <a href={resume.download_url}>
                      <Download className="w-4 h-4" />
                      Download
                    </a>
                  </Button>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => handleDelete(resume.id)}
                    className="flex-1 flex items-center gap-2"
                  >
                    <Trash2 className="w-4 h-4" />
                    Delete
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

