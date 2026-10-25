import Link from "next/link";
import {
  ArrowRight,
  FilePlus2,
  FileText,
  Library,
  Sparkles,
} from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="overview-page">
      <div className="welcome-row">
        <div>
          <p className="section-kicker">Tuesday, October 24</p>
          <h2>Good morning, Jordan.</h2>
          <p className="subtle">
            Let&apos;s make your next application your strongest one yet.
          </p>
        </div>
        <Link href="/dashboard/create-cv" className="primary-button">
          <FilePlus2 size={16} /> Create a CV
        </Link>
      </div>
      <div className="dashboard-stats">
        <div>
          <span>Total CVs</span>
          <strong>—</strong>
          <small>Connect your backend to see your library</small>
        </div>
        <div>
          <span>Latest ATS score</span>
          <strong>—</strong>
          <small>Run an analysis to get your score</small>
        </div>
        <div>
          <span>Designs saved</span>
          <strong>—</strong>
          <small>Import your first reference</small>
        </div>
      </div>
      <section className="onboarding-card">
        <div className="onboarding-icon">
          <Sparkles size={21} />
        </div>
        <div>
          <p className="section-kicker">Your workspace is ready</p>
          <h3>Start with a CV that sounds like you.</h3>
          <p>
            Share your experience once, then tailor it for every opportunity.
            Your data will appear here after connecting the FastAPI backend.
          </p>
          <div className="onboarding-actions">
            <Link href="/dashboard/create-cv" className="primary-button">
              Create your first CV <ArrowRight size={15} />
            </Link>
            <Link href="/dashboard/designs" className="secondary-button">
              Explore designs
            </Link>
          </div>
        </div>
      </section>
      <div className="quick-grid">
        <Link href="/dashboard/cvs" className="quick-card">
          <span>
            <FileText size={18} />
          </span>
          <div>
            <strong>View my CVs</strong>
            <p>Your saved CVs and versions</p>
          </div>
          <ArrowRight size={16} />
        </Link>
        <Link href="/dashboard/ats" className="quick-card">
          <span>
            <Sparkles size={18} />
          </span>
          <div>
            <strong>Run ATS analysis</strong>
            <p>See how your CV matches a role</p>
          </div>
          <ArrowRight size={16} />
        </Link>
        <Link href="/dashboard/designs" className="quick-card">
          <span>
            <Library size={18} />
          </span>
          <div>
            <strong>Design library</strong>
            <p>Manage your visual references</p>
          </div>
          <ArrowRight size={16} />
        </Link>
      </div>
    </div>
  );
}
