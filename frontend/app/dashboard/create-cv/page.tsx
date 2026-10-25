"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowLeft, ArrowRight, Check, FileText, Sparkles } from "lucide-react";
import { apiRequest, ApiError } from "@/lib/api-client";

const steps = [
  "Personal info",
  "Experience",
  "Education",
  "Skills & projects",
  "Target job",
  "Design",
  "Review",
];

type GenerateCVResponse = {
  job_id: string;
  status: string;
  cv: {
    id: string;
    title: string;
  };
  download_url: string;
};

export default function CreateCvPage() {
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<GenerateCVResponse | null>(null);

  const [form, setForm] = useState({
    title: "",
    full_name: "",
    email: "",
    phone: "",
    location: "",
    headline: "",
    summary: "",
    experience: "",
    education: "",
    skills: "",
    projects: "",
    target_job: "",
    job_description: "",
    design_id: "",
  });

  function updateField(field: keyof typeof form, value: string) {
    setForm((previous) => ({
      ...previous,
      [field]: value,
    }));
  }

  async function generateCV() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const payload = {
        title: form.title.trim(),
        personal_info: {
          full_name: form.full_name.trim(),
          email: form.email.trim(),
          phone: form.phone.trim(),
          location: form.location.trim(),
          headline: form.headline.trim(),
          summary: form.summary.trim(),
        },
        experience: form.experience
          .split("\n")
          .map((item) => item.trim())
          .filter(Boolean),
        education: form.education
          .split("\n")
          .map((item) => item.trim())
          .filter(Boolean),
        skills: form.skills
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        projects: form.projects
          .split("\n")
          .map((item) => item.trim())
          .filter(Boolean),
        target_job: form.target_job.trim(),
        job_description: form.job_description.trim(),
        design_id: form.design_id.trim() || null,
      };

      const response = await apiRequest<GenerateCVResponse>(
        "/api/v1/cv-generation/generate",
        {
          method: "POST",
          body: JSON.stringify(payload),
        },
      );

      setResult(response);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError(
          err instanceof Error
            ? err.message
            : "Something went wrong while generating your CV.",
        );
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="wizard-page">
      <div className="wizard-intro">
        <Link href="/dashboard" className="back-link">
          <ArrowLeft size={15} />
          Back to overview
        </Link>

        <p className="section-kicker">Create a CV</p>
        <h2>Let&apos;s build your story.</h2>
        <p className="subtle">Enter your information, then generate your CV.</p>
      </div>

      <div className="wizard-layout">
        <aside className="stepper">
          {steps.map((item, index) => (
            <button
              key={item}
              type="button"
              className={
                index === step
                  ? "step active"
                  : index < step
                    ? "step complete"
                    : "step"
              }
              onClick={() => {
                if (index <= step) setStep(index);
              }}
            >
              <span>{index < step ? <Check size={13} /> : index + 1}</span>
              {item}
            </button>
          ))}
        </aside>

        <section className="wizard-card">
          <div className="wizard-card-header">
            <div>
              <span className="step-count">
                Step {step + 1} of {steps.length}
              </span>
              <h3>{steps[step]}</h3>
            </div>
            <Sparkles size={18} color="#5b5ce2" />
          </div>

          {result ? (
            <div className="step-placeholder">
              <Check size={28} />
              <h4>CV created successfully</h4>
              <p>Your CV has been saved as a draft.</p>
              <p>
                <strong>Title:</strong> {result.cv.title}
              </p>
              <p>
                <strong>CV ID:</strong> {result.cv.id}
              </p>
              <p>
                <strong>Generation status:</strong> {result.status}
              </p>
              <button
                type="button"
                className="secondary-button"
                onClick={() => {
                  setResult(null);
                  setStep(0);
                }}
              >
                Create another CV
              </button>
            </div>
          ) : (
            <>
              {step === 0 && (
                <div className="form-grid">
                  <label className="full">
                    CV title
                    <input
                      required
                      value={form.title}
                      onChange={(e) => updateField("title", e.target.value)}
                      placeholder="e.g. Backend Developer CV"
                    />
                  </label>

                  <label>
                    Full name
                    <input
                      required
                      value={form.full_name}
                      onChange={(e) => updateField("full_name", e.target.value)}
                      placeholder="Your full name"
                    />
                  </label>

                  <label>
                    Email
                    <input
                      type="email"
                      value={form.email}
                      onChange={(e) => updateField("email", e.target.value)}
                      placeholder="you@example.com"
                    />
                  </label>

                  <label>
                    Phone
                    <input
                      value={form.phone}
                      onChange={(e) => updateField("phone", e.target.value)}
                      placeholder="Phone number"
                    />
                  </label>

                  <label>
                    Location
                    <input
                      value={form.location}
                      onChange={(e) => updateField("location", e.target.value)}
                      placeholder="City, country"
                    />
                  </label>

                  <label className="full">
                    Professional headline
                    <input
                      value={form.headline}
                      onChange={(e) => updateField("headline", e.target.value)}
                      placeholder="e.g. Backend Developer"
                    />
                  </label>

                  <label className="full">
                    Professional summary
                    <textarea
                      rows={5}
                      value={form.summary}
                      onChange={(e) => updateField("summary", e.target.value)}
                      placeholder="Your professional background and strengths..."
                    />
                  </label>
                </div>
              )}

              {step === 1 && (
                <div className="form-grid">
                  <label className="full">
                    Work experience
                    <textarea
                      rows={8}
                      value={form.experience}
                      onChange={(e) =>
                        updateField("experience", e.target.value)
                      }
                      placeholder={
                        "Enter one experience per line.\nJob title, company, dates, achievements..."
                      }
                    />
                  </label>
                </div>
              )}

              {step === 2 && (
                <div className="form-grid">
                  <label className="full">
                    Education
                    <textarea
                      rows={6}
                      value={form.education}
                      onChange={(e) => updateField("education", e.target.value)}
                      placeholder={
                        "Enter one education item per line.\nDegree, institution, graduation year..."
                      }
                    />
                  </label>
                </div>
              )}

              {step === 3 && (
                <div className="form-grid">
                  <label className="full">
                    Skills
                    <textarea
                      rows={4}
                      value={form.skills}
                      onChange={(e) => updateField("skills", e.target.value)}
                      placeholder="Python, FastAPI, PostgreSQL, React..."
                    />
                    <small>Separate skills with commas.</small>
                  </label>

                  <label className="full">
                    Projects
                    <textarea
                      rows={6}
                      value={form.projects}
                      onChange={(e) => updateField("projects", e.target.value)}
                      placeholder={
                        "Enter one project per line.\nProject name, technologies, achievements..."
                      }
                    />
                  </label>
                </div>
              )}

              {step === 4 && (
                <div className="form-grid">
                  <label className="full">
                    Target job title
                    <input
                      value={form.target_job}
                      onChange={(e) =>
                        updateField("target_job", e.target.value)
                      }
                      placeholder="e.g. Python Backend Developer"
                    />
                  </label>

                  <label className="full">
                    Job description
                    <textarea
                      rows={8}
                      value={form.job_description}
                      onChange={(e) =>
                        updateField("job_description", e.target.value)
                      }
                      placeholder="Paste the job description to tailor your CV..."
                    />
                  </label>
                </div>
              )}

              {step === 5 && (
                <div className="form-grid">
                  <label className="full">
                    Design ID (optional)
                    <input
                      value={form.design_id}
                      onChange={(e) => updateField("design_id", e.target.value)}
                      placeholder="UUID of an existing CV design"
                    />
                    <small>
                      Leave empty if you want to use the default design.
                    </small>
                  </label>
                </div>
              )}

              {step === 6 && (
                <div className="step-placeholder">
                  <FileText size={24} />
                  <h4>Review your CV information</h4>
                  <p>
                    <strong>Title:</strong> {form.title || "Not provided"}
                  </p>
                  <p>
                    <strong>Name:</strong> {form.full_name || "Not provided"}
                  </p>
                  <p>
                    <strong>Target job:</strong>{" "}
                    {form.target_job || "Not provided"}
                  </p>
                  <p>
                    <strong>Experience entries:</strong>{" "}
                    {form.experience.split("\n").filter((x) => x.trim()).length}
                  </p>
                  <p>
                    <strong>Skills:</strong> {form.skills || "Not provided"}
                  </p>
                </div>
              )}

              {error && (
                <p role="alert" className="error-message">
                  {error}
                </p>
              )}

              <div className="wizard-footer">
                {step > 0 ? (
                  <button
                    type="button"
                    className="secondary-button"
                    disabled={loading}
                    onClick={() => setStep(step - 1)}
                  >
                    Back
                  </button>
                ) : (
                  <span />
                )}

                {step < steps.length - 1 ? (
                  <button
                    type="button"
                    className="primary-button"
                    onClick={() => {
                      setError("");
                      setStep(step + 1);
                    }}
                  >
                    Continue <ArrowRight size={15} />
                  </button>
                ) : (
                  <button
                    type="button"
                    className="primary-button"
                    disabled={loading || !form.title.trim()}
                    onClick={generateCV}
                  >
                    <Sparkles size={15} />
                    {loading ? "Generating..." : "Generate CV"}
                  </button>
                )}
              </div>
            </>
          )}
        </section>
      </div>
    </div>
  );
}
