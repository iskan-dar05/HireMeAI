"""Initial HireMeAI tables."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("clerk_user_id", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("email", sa.String(320), nullable=True),
        sa.Column("full_name", sa.String(200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "cv_designs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("layout_spec", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("original_object_key", sa.String(1024), nullable=True),
        sa.Column("preview_object_key", sa.String(1024), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "cvs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("design_id", sa.Uuid(), sa.ForeignKey("cv_designs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="draft"),
        sa.Column("content", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("pdf_object_key", sa.String(1024), nullable=True),
        sa.Column("job_description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "cv_versions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("cv_id", sa.Uuid(), sa.ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("content", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("pdf_object_key", sa.String(1024), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("cv_id", "version_number", name="uq_cv_version_number"),
    )
    op.create_table(
        "generation_jobs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("cv_id", sa.Uuid(), sa.ForeignKey("cvs.id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("task_type", sa.String(40), nullable=False),
        sa.Column("status", sa.String(24), nullable=False, server_default="PENDING"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

def downgrade():
    op.drop_table("generation_jobs")
    op.drop_table("cv_versions")
    op.drop_table("cvs")
    op.drop_table("cv_designs")
    op.drop_table("users")
