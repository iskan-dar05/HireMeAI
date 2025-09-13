import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/Navbar";
import template1 from "@/assets/template-1.jpg";
import template2 from "@/assets/template-2.jpg";
import template3 from "@/assets/template-3.jpg";

const Templates = () => {
  const templates = [
    {
      id: 1,
      name: "Professional",
      description: "Clean and modern design perfect for corporate roles",
      image: template1,
      category: "Professional"
    },
    {
      id: 2,
      name: "Creative",
      description: "Bold design with creative elements for design roles",
      image: template2,
      category: "Creative"
    },
    {
      id: 3,
      name: "Executive",
      description: "Sophisticated layout for senior positions",
      image: template3,
      category: "Executive"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <section className="py-16 px-6">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Choose Your <span className="bg-gradient-primary bg-clip-text text-transparent">Template</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Professional templates designed to make you stand out
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {templates.map((template) => (
              <Card key={template.id} className="group cursor-pointer transition-all hover:shadow-elegant bg-gradient-card">
                <CardContent className="p-6">
                  <div className="aspect-[3/4] mb-4 overflow-hidden rounded-lg bg-muted">
                    <img 
                      src={template.image} 
                      alt={template.name}
                      className="w-full h-full object-cover transition-transform group-hover:scale-105"
                    />
                  </div>
                  <div className="space-y-2 mb-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold">{template.name}</h3>
                      <span className="text-xs px-2 py-1 bg-accent rounded-full text-accent-foreground">
                        {template.category}
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground">{template.description}</p>
                  </div>
                  <Button className="w-full bg-gradient-primary hover:shadow-glow transition-all">
                    Use This Template
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Templates;