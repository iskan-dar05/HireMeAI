import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Link } from "react-router-dom";
import Navbar from "@/components/Navbar";
import { ArrowRight, FileText, Zap, Download, Star } from "lucide-react";
import template1 from "@/assets/template-1.jpg";
import template2 from "@/assets/template-2.jpg";
import template3 from "@/assets/template-3.jpg";

const Index = () => {
  const features = [
    {
      icon: <FileText className="h-8 w-8 text-primary" />,
      title: "Professional Templates",
      description: "Choose from dozens of professionally designed templates"
    },
    {
      icon: <Zap className="h-8 w-8 text-primary" />,
      title: "Quick Generation",
      description: "Create your CV in minutes with our intuitive builder"
    },
    {
      icon: <Download className="h-8 w-8 text-primary" />,
      title: "Export Ready",
      description: "Download in PDF format, ready for job applications"
    }
  ];

  const templates = [
    { name: "Professional", image: template1 },
    { name: "Creative", image: template2 },
    { name: "Executive", image: template3 }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative py-20 px-6 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-hero opacity-5"></div>
        <div className="container mx-auto text-center relative">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              Build Your Perfect{" "}
              <span className="bg-gradient-primary bg-clip-text text-transparent">
                Resume
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
              Create professional resumes that get you hired. Choose from beautiful templates and build your CV in minutes.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild className="bg-gradient-primary hover:shadow-glow transition-all text-lg px-8 py-6">
                <Link to="/create-resume">
                  Start Building <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" asChild className="text-lg px-8 py-6 hover:shadow-card transition-all">
                <Link to="/templates">
                  View Templates
                </Link>
              </Button>
            </div>
            
            <div className="flex items-center justify-center gap-2 mt-8 text-sm text-muted-foreground">
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                ))}
              </div>
              <span>Trusted by 10,000+ job seekers</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6 bg-muted/30">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why Choose Our <span className="bg-gradient-primary bg-clip-text text-transparent">CV Builder</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Everything you need to create a professional resume that stands out
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center shadow-card hover:shadow-elegant transition-all bg-gradient-card">
                <CardContent className="p-8">
                  <div className="flex justify-center mb-6">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Templates Preview */}
      <section className="py-20 px-6">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Beautiful <span className="bg-gradient-primary bg-clip-text text-transparent">Templates</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Professional designs that make you stand out from the crowd
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {templates.map((template, index) => (
              <Card key={index} className="group cursor-pointer transition-all hover:shadow-elegant bg-gradient-card">
                <CardContent className="p-6">
                  <div className="aspect-[3/4] mb-4 overflow-hidden rounded-lg bg-muted">
                    <img 
                      src={template.image} 
                      alt={template.name}
                      className="w-full h-full object-cover transition-transform group-hover:scale-105"
                    />
                  </div>
                  <h3 className="text-center font-semibold">{template.name}</h3>
                </CardContent>
              </Card>
            ))}
          </div>
          
          <div className="text-center">
            <Button size="lg" variant="outline" asChild className="hover:shadow-card transition-all">
              <Link to="/templates">
                View All Templates <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 bg-gradient-hero relative overflow-hidden">
        <div className="absolute inset-0 bg-primary/5"></div>
        <div className="container mx-auto text-center relative">
          <h2 className="text-3xl md:text-4xl font-bold mb-6 text-primary-foreground">
            Ready to Build Your Dream Career?
          </h2>
          <p className="text-lg mb-8 text-primary-foreground/80 max-w-2xl mx-auto">
            Join thousands of successful job seekers who found their dream job with our professional resume builder.
          </p>
          <Button size="lg" asChild className="bg-white text-primary hover:bg-white/90 hover:shadow-glow transition-all text-lg px-8 py-6">
            <Link to="/signup">
              Get Started Free <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Index;