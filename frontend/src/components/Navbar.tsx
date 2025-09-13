import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { FileText, User, LogIn } from "lucide-react";

const Navbar = () => {
  const location = useLocation();
  const onLoginPage = location.pathname === "/login";
  const onSignupPage = location.pathname === "/signup";
  return (
    <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-6">
        <Link to="/" className="flex items-center space-x-2">
          <FileText className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            HireMeAI
          </span>
        </Link>
        
        <div className="hidden md:flex items-center space-x-6">
          <Link to="/" className="text-sm font-medium hover:text-primary transition-colors">
            Home
          </Link>
          <Link to="/templates" className="text-sm font-medium hover:text-primary transition-colors">
            Templates
          </Link>
          <Link to="/create" className="text-sm font-medium hover:text-primary transition-colors">
            Create CV
          </Link>
        </div>

        <div className="flex items-center space-x-3">
          {!onLoginPage && (
            <Button variant="ghost" size="sm" asChild>
              <Link to="/login">
                <LogIn className="h-4 w-4 mr-2" />
                Login
              </Link>
            </Button>
          )}
          
          {!onSignupPage && (
            <Button size="sm" asChild className="bg-gradient-primary hover:shadow-glow transition-all">
              <Link to="/signup">
                <User className="h-4 w-4 mr-2" />
                Sign Up
              </Link>
            </Button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;