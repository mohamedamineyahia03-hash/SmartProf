"""Library-service schema. This service is the content factory: it owns crawling,
license classification, AI generation, and review — never the Main App's DB.

The `exercise.generation_run_id` foreign key is NOT NULL by design: there is no
insert path that can create an exercise without a generation_run (which itself
requires a source). This is what makes "every exercise is AI-generated from a
source, never copied verbatim" a schema-level fact rather than a policy note.
"""

from db import db

LICENSE_STATUSES = ("explicit_open", "unlicensed", "proprietary_excluded")
SOURCE_STATUSES = ("pending_classification", "classified", "rejected", "used_for_generation")
REGION_SCOPES = (
    "tunisia_official",
    "tunisia_web",
    "fr_ministry_approved",
    "fr_web",  # French pedagogy sites that claim programme-Éducation-nationale alignment but aren't the Ministry itself
    "uk_approved",
    "international_aligned",  # any country's resource, used only where its topic genuinely matches the Tunisian program
)
CONTENT_LANGUAGES = ("ar", "fr", "en")
CRAWL_TRIGGERS = ("scheduled", "demand_signal", "manual")
GENERATION_STATUSES = ("success", "failed", "flagged_for_review")
REVIEW_STATUSES = ("auto_passed_schema", "pending_human_review", "approved", "rejected")
EXERCISE_STATUSES = ("draft", "published", "retired")


class CrawlJob(db.Model):
    __tablename__ = "crawl_job"

    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime, server_default=db.func.now())
    finished_at = db.Column(db.DateTime, nullable=True)
    trigger = db.Column(db.Enum(*CRAWL_TRIGGERS, name="crawl_trigger"), nullable=False, default="manual")
    target_subject = db.Column(db.String(16), nullable=True)
    target_level = db.Column(db.String(1), nullable=True)
    target_region_scope = db.Column(db.Enum(*REGION_SCOPES, name="region_scope_job"), nullable=True)
    sources_found = db.Column(db.Integer, nullable=False, default=0)
    sources_accepted = db.Column(db.Integer, nullable=False, default=0)

    sources = db.relationship("Source", backref="crawl_job")


class Source(db.Model):
    __tablename__ = "source"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    title = db.Column(db.String(512), nullable=True)
    discovered_at = db.Column(db.DateTime, server_default=db.func.now())
    crawl_job_id = db.Column(db.Integer, db.ForeignKey("crawl_job.id"), nullable=True)

    license_status = db.Column(db.Enum(*LICENSE_STATUSES, name="license_status"), nullable=False)
    license_detail = db.Column(db.Text, nullable=True)

    subject_code = db.Column(db.String(16), nullable=False)
    level_code = db.Column(db.String(1), nullable=False)
    domain_hint = db.Column(db.String(64), nullable=True)
    trimester_hint = db.Column(db.String(2), nullable=True)
    region_scope = db.Column(db.Enum(*REGION_SCOPES, name="region_scope_source"), nullable=False)

    # Used ONLY as generation input (Section: pipeline step "Generate") — never
    # served to end users directly, never copied into exercise.content.
    content_snapshot = db.Column(db.Text, nullable=True)

    status = db.Column(db.Enum(*SOURCE_STATUSES, name="source_status"), nullable=False, default="pending_classification")

    generation_runs = db.relationship("GenerationRun", backref="source")


class GenerationRun(db.Model):
    __tablename__ = "generation_run"

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey("source.id"), nullable=False)
    model_provider = db.Column(db.String(32), nullable=False, default="anthropic")
    model_name = db.Column(db.String(64), nullable=False)
    prompt_template_version = db.Column(db.String(32), nullable=False)
    started_at = db.Column(db.DateTime, server_default=db.func.now())
    finished_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(*GENERATION_STATUSES, name="generation_status"), nullable=False, default="success")
    raw_model_output = db.Column(db.Text, nullable=True)

    exercises = db.relationship("Exercise", backref="generation_run")


class Exercise(db.Model):
    __tablename__ = "exercise"

    id = db.Column(db.Integer, primary_key=True)

    # Structural enforcement: cannot exist without a generation_run.
    generation_run_id = db.Column(db.Integer, db.ForeignKey("generation_run.id"), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey("source.id"), nullable=True)  # traceability only

    subject_code = db.Column(db.String(16), nullable=False)
    level_code = db.Column(db.String(1), nullable=False)
    trimester = db.Column(db.String(2), nullable=False)
    domain_code = db.Column(db.String(64), nullable=False)
    skill_code = db.Column(db.String(64), nullable=False)
    exercise_format = db.Column(db.String(32), nullable=False)
    difficulty = db.Column(db.String(16), nullable=False, default="en_cours")

    # Single-language content — no bilingual duplication. Language is fixed
    # per subject: "ar" for math/science/ar, "fr" for the fr subject (French
    # stays entirely in French, not translated), "en" for the en subject
    # (same for English) — see generate_exercise.LANGUAGE_BY_SUBJECT. The app
    # interface itself is Arabic-only and has no language switcher; this
    # field is unrelated to that — it's what language THIS exercise's own
    # content is written in.
    language = db.Column(db.Enum(*CONTENT_LANGUAGES, name="content_language"), nullable=False)
    content = db.Column(db.JSON, nullable=False)

    license = db.Column(db.String(32), nullable=False, default="SmartProf")

    review_status = db.Column(
        db.Enum(*REVIEW_STATUSES, name="review_status"), nullable=False, default="pending_human_review"
    )
    reviewed_by = db.Column(db.String(128), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.Enum(*EXERCISE_STATUSES, name="exercise_status"), nullable=False, default="draft")
    curriculum_schema_version = db.Column(db.String(16), nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
