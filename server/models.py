from db import db


class CurriculumLevel(db.Model):
    __tablename__ = "curriculum_level"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(1), unique=True, nullable=False)  # "1".."5"
    label_fr = db.Column(db.String(64), nullable=False)
    label_ar = db.Column(db.String(64), nullable=False)


class CurriculumSubject(db.Model):
    __tablename__ = "curriculum_subject"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, nullable=False)  # math/fr/science/en/ar
    label_fr = db.Column(db.String(64), nullable=False)
    label_ar = db.Column(db.String(64), nullable=False)
    # Which level codes ("1".."5") this subject is free at — everything else
    # requires an unlock. Per-level rather than a "1-2 vs 3-5" band so a
    # subject can be free at some levels within a band and paid at others
    # (e.g. English free at 4-5 but still paid at 3).
    free_levels = db.Column(db.JSON, nullable=False, default=list)


class CurriculumDomain(db.Model):
    __tablename__ = "curriculum_domain"

    id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.Integer, db.ForeignKey("curriculum_level.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("curriculum_subject.id"), nullable=False)
    code = db.Column(db.String(64), nullable=False)
    name_fr = db.Column(db.String(128), nullable=False)
    name_ar = db.Column(db.String(128), nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    # "programme" = a normal trimester-gated section (the section tree groups
    # it under T1/T2/T3, see CurriculumDomainTrimester). "expression" = an
    # independent section shown outside the trimester tabs (Expression orale
    # et écrite, Récitation) — no trimester rows are created for it.
    category = db.Column(db.String(16), nullable=False, default="programme")

    level = db.relationship("CurriculumLevel")
    subject = db.relationship("CurriculumSubject")
    skills = db.relationship(
        "CurriculumSkill",
        backref="domain",
        cascade="all, delete-orphan",
        order_by="CurriculumSkill.sort_order",
    )
    trimesters = db.relationship(
        "CurriculumDomainTrimester", backref="domain", cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("level_id", "subject_id", "code", name="uq_domain_level_subject_code"),
    )


class CurriculumDomainTrimester(db.Model):
    __tablename__ = "curriculum_domain_trimester"

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey("curriculum_domain.id"), nullable=False)
    trimester = db.Column(db.String(2), nullable=False)  # T1/T2/T3

    __table_args__ = (
        db.UniqueConstraint("domain_id", "trimester", name="uq_domain_trimester"),
    )


class CurriculumSkill(db.Model):
    __tablename__ = "curriculum_skill"

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey("curriculum_domain.id"), nullable=False)
    code = db.Column(db.String(64), nullable=False)
    name_fr = db.Column(db.String(128), nullable=False)
    name_ar = db.Column(db.String(128), nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    exercise_formats = db.relationship(
        "CurriculumExerciseFormat", backref="skill", cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("domain_id", "code", name="uq_skill_domain_code"),
    )


class CurriculumExerciseFormat(db.Model):
    __tablename__ = "curriculum_exercise_format"

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("curriculum_skill.id"), nullable=False)
    format_code = db.Column(db.String(32), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("skill_id", "format_code", name="uq_format_skill_code"),
    )


# --- Phase 4 stubs (schema-first, not yet wired to routes) ---


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    locale_pref = db.Column(db.String(8), default="fr")
    # Bouche-à-oreille : code court unique attribué à l'inscription, partagé
    # via un lien (?ref=CODE). referred_by_user_id trace qui a amené qui, dès
    # maintenant — la récompense (mois offert, matière débloquée...) sera
    # décidée avec le reste de la tarification, mais la relation de parrainage
    # est déjà capturée pour pouvoir être récompensée rétroactivement.
    referral_code = db.Column(db.String(12), unique=True, nullable=True)
    referred_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    children = db.relationship("ChildProfile", backref="user", cascade="all, delete-orphan")


class ChildProfile(db.Model):
    __tablename__ = "child_profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    display_name = db.Column(db.String(64), nullable=False)
    level_code = db.Column(db.String(1), nullable=False)


class Entitlement(db.Model):
    __tablename__ = "entitlement"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    kind = db.Column(db.String(32), nullable=False, default="subject_unlock")
    subject_code = db.Column(db.String(16), nullable=False)
    level_code = db.Column(db.String(1), nullable=False)
    granted_at = db.Column(db.DateTime, server_default=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=True)  # set for annual subscriptions
    source = db.Column(db.String(16), nullable=False, default="purchase_onetime")


class DiagnosticResult(db.Model):
    __tablename__ = "diagnostic_result"

    id = db.Column(db.Integer, primary_key=True)
    child_profile_id = db.Column(db.Integer, db.ForeignKey("child_profile.id"), nullable=False)
    level_code = db.Column(db.String(1), nullable=False)
    subject_code = db.Column(db.String(16), nullable=False)
    skill_code = db.Column(db.String(64), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    mastery_level = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class LibraryCacheExercise(db.Model):
    """Local mirror of published exercises pulled from the external library-service.
    Populated by sync/library_sync.py — never written to directly by request handlers."""

    __tablename__ = "library_cache_exercise"

    id = db.Column(db.Integer, primary_key=True)
    library_exercise_id = db.Column(db.Integer, unique=True, nullable=False)
    level_code = db.Column(db.String(1), nullable=False)
    subject_code = db.Column(db.String(16), nullable=False)
    trimester = db.Column(db.String(2), nullable=False)
    domain_code = db.Column(db.String(64), nullable=False)
    skill_code = db.Column(db.String(64), nullable=False)
    exercise_format = db.Column(db.String(32), nullable=False)
    difficulty = db.Column(db.String(16), nullable=False)
    # Single-language content — Arabic for math/science/ar, French for fr,
    # English for en. No bilingual duplication; the app interface itself is
    # Arabic-only with no language switcher (see generate_exercise.py in
    # library-service for LANGUAGE_BY_SUBJECT).
    language = db.Column(db.String(2), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    # "auto" = exact-match graded against content["answer"] (or each
    # sub_questions[i]["answer"]), the historical default. "open" = no
    # canonical answer — expression écrite / récitation content — the
    # child's response is recorded but never scored; content["model_answer"]
    # is shown afterward as a self-check reference only.
    grading_mode = db.Column(db.String(8), nullable=False, default="auto")
    license = db.Column(db.String(32), nullable=False, default="SmartProf")
    synced_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class Session(db.Model):
    """An exam-style session: a fixed, varied batch of exercises drawn from one
    curriculum section (domain) and built all at once — see
    server/session_engine.build_exam_session(). The child answers every
    question with no immediate feedback; the corrigé (score + full answer
    key) is only available once every exercise has an answer, via
    GET /api/session/<id>/corrige. child_profile_id is nullable for now —
    accounts don't exist yet (Phase 4), so sessions are anonymous until
    then."""

    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)
    child_profile_id = db.Column(db.Integer, db.ForeignKey("child_profile.id"), nullable=True)
    level_code = db.Column(db.String(1), nullable=False)
    subject_code = db.Column(db.String(16), nullable=False)
    trimester = db.Column(db.String(2), nullable=False)
    domain_code = db.Column(db.String(64), nullable=False)  # the section this session was started from
    exercise_ids = db.Column(db.JSON, nullable=False)  # the full batch, fixed at session creation
    answers = db.Column(db.JSON, nullable=False, default=dict)  # {exercise_id: {given, correct, skill}}
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    completed_at = db.Column(db.DateTime, nullable=True)
    # Anti-abuse for the free-trial-per-subject mechanic: a new child profile
    # (or a whole new account) is free to create, so without this a parent
    # could keep re-triggering "essai gratuit" on the same subject forever.
    # is_trial marks the session that actually consumed a free look; client_ip
    # (best-effort, see app._client_ip) lets later trial checks recognize the
    # same device trying again under a different child/account. Not a
    # fraud-proof fingerprint — shared NATs/VPNs/carrier IPs can collide, and
    # mobile IPs can rotate — just a reasonable first line of defense.
    client_ip = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    is_trial = db.Column(db.Boolean, nullable=False, default=False)
