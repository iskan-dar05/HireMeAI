import Link from "next/link";
import { SignIn } from "@clerk/nextjs";
import { Sparkles } from "lucide-react";

export default function SignInPage() {
  return (
    <main className="auth-page">
      <div className="auth-card">
        <Link href="/" className="brand">
          <span className="brand-mark">
            <Sparkles size={16} />
          </span>
          HireMe<span className="brand-accent">AI</span>
        </Link>

        <div className="auth-heading">
          <h1>Welcome back</h1>
          <p>Sign in to continue building your next opportunity.</p>
        </div>

        <div className="clerk-auth-container">
          <SignIn
            routing="path"
            path="/sign-in"
            signUpUrl="/sign-up"
            forceRedirectUrl="/dashboard"
            appearance={{
              layout: {
                socialButtonsPlacement: "top",
                socialButtonsVariant: "blockButton",
                showOptionalFields: false,
              },
              variables: {
                colorPrimary: "#183D3A",
                colorText: "#183D3A",
                colorTextSecondary: "#55716D",
                colorBackground: "#FFFFFF",
                colorInputBackground: "#FFFFFF",
                colorInputText: "#183D3A",
                borderRadius: "12px",
                fontFamily: "inherit",
              },
              elements: {
                rootBox: {
                  width: "100%",
                  margin: "0 auto",
                },
                cardBox: {
                  width: "100%",
                  maxWidth: "100%",
                  boxShadow: "none",
                },
                card: {
                  width: "100%",
                  maxWidth: "100%",
                  padding: "0",
                  gap: "20px",
                  boxShadow: "none",
                  border: "none",
                  background: "transparent",
                },
                header: {
                  display: "none",
                },
                main: {
                  width: "100%",
                  gap: "16px",
                },
                socialButtons: {
                  width: "100%",
                },
                socialButtonsBlockButton: {
                  minHeight: "46px",
                  borderRadius: "12px",
                  border: "1px solid #B9CCC5",
                  backgroundColor: "#FFFFFF",
                  color: "#183D3A",
                  boxShadow: "none",
                  fontSize: "14px",
                  fontWeight: "500",
                },
                socialButtonsBlockButtonText: {
                  color: "#183D3A",
                  fontWeight: "500",
                },
                dividerRow: {
                  margin: "8px 0",
                },
                dividerLine: {
                  backgroundColor: "#DCE7E3",
                },
                dividerText: {
                  color: "#829490",
                  fontSize: "12px",
                },
                form: {
                  gap: "16px",
                },
                formFieldRow: {
                  gap: "7px",
                },
                formFieldLabel: {
                  color: "#183D3A",
                  fontSize: "13px",
                  fontWeight: "600",
                  marginBottom: "7px",
                },
                formFieldInput: {
                  width: "100%",
                  minHeight: "46px",
                  padding: "0 14px",
                  borderRadius: "10px",
                  border: "1px solid #DCE5E1",
                  backgroundColor: "#FFFFFF",
                  color: "#183D3A",
                  fontSize: "14px",
                  opacity: "1",
                  visibility: "visible",
                  display: "block",
                  boxShadow: "none",
                },
                formFieldInputShowPasswordButton: {
                  color: "#55716D",
                },
                formFieldHintText: {
                  color: "#55716D",
                  fontSize: "12px",
                },
                formFieldErrorText: {
                  color: "#B42318",
                  fontSize: "12px",
                },
                formButtonPrimary: {
                  width: "100%",
                  minHeight: "48px",
                  borderRadius: "12px",
                  backgroundColor: "#183D3A",
                  color: "#FFFFFF",
                  fontSize: "14px",
                  fontWeight: "600",
                  boxShadow: "none",
                },
                footer: {
                  display: "none",
                },
                footerAction: {
                  display: "none",
                },
                identityPreview: {
                  borderRadius: "12px",
                  border: "1px solid #DCE7E3",
                },
              },
            }}
          />
        </div>

        <p className="auth-footer">
          New to HireMeAI? <Link href="/sign-up">Create an account</Link>
        </p>
      </div>
    </main>
  );
}
