import Link from "next/link";
import {
  ArrowRight,
  Check,
  FileText,
  Layers3,
  LineChart,
  Palette,
  Sparkles,
  Target,
  WandSparkles,
} from "lucide-react";

const features = [
  {
    icon: WandSparkles,
    title: "AI CV generation",
    text: "Turn your experience into a polished, role-ready CV in minutes.",
  },
  {
    icon: Target,
    title: "Job tailoring",
    text: "Tune every section against a specific job description without losing your voice.",
  },
  {
    icon: LineChart,
    title: "ATS analysis",
    text: "Get a clear compatibility signal and practical suggestions to improve your match.",
  },
  {
    icon: Palette,
    title: "Design extraction",
    text: "Bring a reference layout into your own reusable design library.",
  },
];

export default function Page() {
  return (
    <main className="marketing-page">
      <nav className="marketing-nav">
        <Link href="/" className="brand">
          <span className="brand-mark">
            <Sparkles size={16} />
          </span>
          HireMe<span className="brand-accent">AI</span>
        </Link>
        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How it works</a>
          <a href="#faq">FAQ</a>
        </div>
        <div className="nav-cta">
          <Link href="/sign-in" className="text-button">
            Sign in
          </Link>
          <Link href="/sign-up" className="primary-button">
            Get started <ArrowRight size={15} />
          </Link>
        </div>
      </nav>
      <section className="hero-section">
        <div className="hero-copy">
          <div className="pill">
            <span className="pill-dot" /> Your next opportunity starts here
          </div>
          <h1>
            A CV that gets you <span>closer to yes.</span>
          </h1>
          <p>
            Create a sharper, more confident CV with AI. Tailor it to every
            role, understand your ATS score, and show up ready.
          </p>
          <div className="hero-actions">
            <Link href="/sign-up" className="primary-button large">
              Build my CV <ArrowRight size={17} />
            </Link>
            <a href="#features" className="secondary-button large">
              Explore features
            </a>
          </div>
          <div className="trusted-row">
            <div className="avatar-stack">
              <span>AM</span>
              <span>RK</span>
              <span>SL</span>
              <span>+2k</span>
            </div>
            <span>Built for ambitious job seekers</span>
          </div>
        </div>
        <div className="hero-visual">
          <div className="glow" />
          <div className="cv-window">
            <div className="window-bar">
              <span />
              <span />
              <span />
              <div className="window-label">CV preview</div>
            </div>
            <div className="cv-paper">
              <div className="paper-header">
                <div>
                  <div className="paper-name">Jordan Davis</div>
                  <div className="paper-role">Product designer</div>
                </div>
                <div className="paper-contact">
                  jordan@example.com
                  <br />
                  New York, NY
                </div>
              </div>
              <div className="paper-rule" />
              <div className="paper-grid">
                <div>
                  <div className="paper-section-title">Experience</div>
                  <div className="paper-line strong" />
                  <div className="paper-line wide" />
                  <div className="paper-line" />
                  <div className="paper-line short" />
                  <div className="paper-section-title second">Education</div>
                  <div className="paper-line strong" />
                  <div className="paper-line wide" />
                </div>
                <div className="paper-side">
                  <div className="paper-section-title">Skills</div>
                  <div className="skill-pills">
                    <i />
                    <i />
                    <i />
                    <i />
                    <i />
                  </div>
                  <div className="paper-section-title second">Profile</div>
                  <div className="paper-line" />
                  <div className="paper-line" />
                  <div className="paper-line short" />
                </div>
              </div>
              <div className="ai-note">
                <span className="ai-note-icon">
                  <Sparkles size={13} />
                </span>
                <div>
                  <strong>AI suggestion</strong>
                  <span>Make your impact measurable here.</span>
                </div>
                <Check size={15} />
              </div>
            </div>
          </div>
        </div>
      </section>
      <section className="logo-strip">
        <span>Designed for the way you work</span>
        <div>
          <strong>northstar</strong>
          <strong>vertex</strong>
          <strong>arc</strong>
          <strong>pioneer</strong>
          <strong>clearpath</strong>
        </div>
      </section>
      <section id="features" className="section-block">
        <div className="section-heading">
          <div>
            <p className="section-kicker">Everything you need</p>
            <h2>Less formatting. More getting noticed.</h2>
          </div>
          <p>
            From first draft to final export, HireMeAI keeps the work focused on
            what matters: your story and the role ahead.
          </p>
        </div>
        <div className="feature-grid">
          {features.map((feature) => (
            <article className="feature-card" key={feature.title}>
              <span className="feature-icon">
                <feature.icon size={19} />
              </span>
              <h3>{feature.title}</h3>
              <p>{feature.text}</p>
              <ArrowRight className="feature-arrow" size={17} />
            </article>
          ))}
        </div>
      </section>
      <section id="how-it-works" className="steps-section">
        <div className="section-heading centered">
          <p className="section-kicker">A clearer process</p>
          <h2>From blank page to apply-ready.</h2>
          <p>One focused workflow for every version of your career story.</p>
        </div>
        <div className="steps-grid">
          <div>
            <span>01</span>
            <h3>Build your base</h3>
            <p>
              Add your experience once. HireMeAI helps you shape it into a
              strong foundation.
            </p>
          </div>
          <div>
            <span>02</span>
            <h3>Match the role</h3>
            <p>
              Paste a job description and get targeted suggestions that keep
              your voice intact.
            </p>
          </div>
          <div>
            <span>03</span>
            <h3>Send with confidence</h3>
            <p>
              Review the result, export a polished PDF, and move on to the next
              opportunity.
            </p>
          </div>
        </div>
      </section>
      <section className="cta-section">
        <div>
          <p className="section-kicker">Ready when you are</p>
          <h2>Your best work deserves a better first impression.</h2>
          <p>Start with a smarter CV workflow today.</p>
        </div>
        <Link href="/sign-up" className="primary-button large">
          Build my CV <ArrowRight size={17} />
        </Link>
      </section>
      <footer className="marketing-footer">
        <Link href="/" className="brand">
          <span className="brand-mark">
            <Sparkles size={14} />
          </span>
          HireMe<span className="brand-accent">AI</span>
        </Link>
        <span>© 2025 HireMeAI. Your work, better represented.</span>
        <div>
          <a href="#features">Features</a>
          <a href="#faq">Privacy</a>
          <a href="#faq">Contact</a>
        </div>
      </footer>
    </main>
  );
}
