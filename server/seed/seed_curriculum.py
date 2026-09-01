"""One-time/idempotent import of curriculum data into the generalized DB schema.

Full-detail curriculum (domains -> skills -> exercise_formats, bilingual)
exists for level 1 of Math, Arabic, and Science. Math and Science also have a
domain-only skeleton for levels 2-5 (each domain doubles as its own single
skill — no finer breakdown authored yet). Français and Anglais still have
zero domains at any level: content authoring for those hasn't started.
"""

import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # server/

from app import app  # noqa: E402
from db import db  # noqa: E402
from models import (  # noqa: E402
    CurriculumDomain,
    CurriculumDomainTrimester,
    CurriculumExerciseFormat,
    CurriculumLevel,
    CurriculumSkill,
    CurriculumSubject,
)

LEVELS = [
    ("1", "1ère année", "السنة الأولى"),
    ("2", "2ème année", "السنة الثانية"),
    ("3", "3ème année", "السنة الثالثة"),
    ("4", "4ème année", "السنة الرابعة"),
    ("5", "5ème année", "السنة الخامسة"),
]

ALL_LEVELS = ["1", "2", "3", "4", "5"]

# code, label_fr, label_ar, free_levels
SUBJECTS = [
    ("math", "Mathématiques", "الرياضيات", ALL_LEVELS),
    ("science", "Éveil scientifique", "الإيقاظ العلمي", ALL_LEVELS),
    ("ar", "Arabe", "العربية", ALL_LEVELS),
    ("fr", "Français", "الفرنسية", ["3", "4", "5"]),
    ("en", "Anglais", "الإنجليزية", ["4", "5"]),  # paid unlock at levels 1-2-3
]

MATH_SKELETON = {
    "2": {
        "T1": ["Nombres", "Addition", "Soustraction", "Multiplication", "Problèmes"],
        "T2": ["Nombres", "Multiplication", "Division", "Mesures", "Problèmes"],
        "T3": ["Calcul", "Géométrie", "Mesures", "Problèmes"],
    },
    "3": {
        "T1": ["Nombres", "Calcul", "Multiplication", "Division", "Problèmes"],
        "T2": ["Fractions", "Mesures", "Géométrie", "Problèmes"],
        "T3": ["Calcul", "Géométrie", "Mesures", "Problèmes"],
    },
    "4": {
        "T1": ["Nombres", "Calcul", "Fractions", "Problèmes"],
        "T2": ["Fractions", "Mesures", "Géométrie", "Problèmes"],
        "T3": ["Calcul", "Géométrie", "Mesures", "Problèmes"],
    },
    "5": {
        "T1": ["Nombres", "Calcul", "Fractions", "Problèmes"],
        "T2": ["Fractions", "Décimaux", "Mesures", "Géométrie", "Problèmes"],
        "T3": ["Calcul", "Géométrie", "Mesures", "Problèmes"],
    },
}

# Level 1 Math domain -> trimester(s), lifted from the legacy SKILLS_MATRIX.
MATH1_TRIMESTERS = {
    "T1": ["pre_numeric", "numeration", "calcul"],
    "T2": ["numeration", "calcul", "mesure", "problemes"],
    "T3": ["espace_geometrie", "mesure", "problemes"],
}

# Level 1 Arabic domain -> trimester(s): letters first, reading from T2,
# comprehension/expression/writing consolidated in T3.
ARABIC1_TRIMESTERS = {
    "T1": ["huruf"],
    "T2": ["huruf", "qiraa"],
    "T3": ["qiraa", "fahm", "taabir", "kitaba"],
}

SCIENCE_SKELETON = {
    "2": {
        "T1": ["Le corps humain", "Les animaux"],
        "T2": ["Les plantes", "L'alimentation"],
        "T3": ["L'eau", "Les saisons"],
    },
    "3": {
        "T1": ["Les organes des sens", "La respiration"],
        "T2": ["Les plantes et leur croissance", "L'alimentation et la santé"],
        "T3": ["Les états de la matière", "L'environnement"],
    },
    "4": {
        "T1": ["Le corps humain", "Les animaux et leur milieu"],
        "T2": ["Les plantes: reproduction", "Les matériaux"],
        "T3": ["L'électricité simple", "Le ciel et la Terre"],
    },
    "5": {
        "T1": ["Le corps humain: circulation", "Écosystèmes"],
        "T2": ["Les changements d'état de la matière", "Les forces et mouvements"],
        "T3": ["L'énergie", "Protection de l'environnement"],
    },
}

# Level 1 Science domain -> trimester(s): the body and living things first,
# surroundings/water mid-year, seasons wrap up the year.
SCIENCE1_TRIMESTERS = {
    "T1": ["corps_humain", "etres_vivants"],
    "T2": ["etres_vivants", "environnement", "eau"],
    "T3": ["eau", "saisons"],
}

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MATH1_CURRICULUM_PATH = os.path.join(REPO_ROOT, "data", "math1", "math1_curriculum.json")
ARABIC1_CURRICULUM_PATH = os.path.join(REPO_ROOT, "data", "arabic1", "arabic1_curriculum.json")
SCIENCE1_CURRICULUM_PATH = os.path.join(REPO_ROOT, "data", "science1", "science1_curriculum.json")


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()


def seed_levels_and_subjects():
    levels = {}
    for code, label_fr, label_ar in LEVELS:
        row = CurriculumLevel.query.filter_by(code=code).first()
        if row is None:
            row = CurriculumLevel(code=code, label_fr=label_fr, label_ar=label_ar)
            db.session.add(row)
        levels[code] = row

    subjects = {}
    for code, label_fr, label_ar, free_levels in SUBJECTS:
        row = CurriculumSubject.query.filter_by(code=code).first()
        if row is None:
            row = CurriculumSubject(
                code=code,
                label_fr=label_fr,
                label_ar=label_ar,
                free_levels=free_levels,
            )
            db.session.add(row)
        subjects[code] = row

    db.session.commit()
    return levels, subjects


def seed_domain_curriculum(levels, subjects, level_code, subject_code, curriculum_path, trimester_map):
    """Imports a full-granularity curriculum JSON (domains -> skills ->
    exercise_formats, bilingual) for one level/subject — the pattern shared by
    math1 and every subsequent subject seeded at full detail."""
    level = levels[level_code]
    subject = subjects[subject_code]

    if CurriculumDomain.query.filter_by(level_id=level.id, subject_id=subject.id).first():
        return

    with open(curriculum_path, encoding="utf-8") as f:
        curriculum = json.load(f)

    domain_trimesters = {}
    for trimester, domain_codes in trimester_map.items():
        for domain_code in domain_codes:
            domain_trimesters.setdefault(domain_code, []).append(trimester)

    for sort_order, domain_data in enumerate(curriculum["domains"]):
        domain = CurriculumDomain(
            level_id=level.id,
            subject_id=subject.id,
            code=domain_data["id"],
            name_fr=domain_data["name_fr"],
            name_ar=domain_data["name_ar"],
            sort_order=sort_order,
        )
        db.session.add(domain)
        db.session.flush()

        for trimester in domain_trimesters.get(domain_data["id"], ["T1"]):
            db.session.add(CurriculumDomainTrimester(domain_id=domain.id, trimester=trimester))

        for skill_order, skill_code in enumerate(domain_data["skills"]):
            # No authored display label exists per-skill yet, only the code itself.
            skill = CurriculumSkill(
                domain_id=domain.id,
                code=skill_code,
                name_fr=skill_code.replace("_", " "),
                name_ar=skill_code.replace("_", " "),
                sort_order=skill_order,
            )
            db.session.add(skill)
            db.session.flush()

            for format_code in domain_data["exercise_formats"].get(skill_code, []):
                db.session.add(
                    CurriculumExerciseFormat(skill_id=skill.id, format_code=format_code)
                )

    db.session.commit()


def seed_skeleton_curriculum(levels, subjects, subject_code, skeleton):
    """Domain-name-only curriculum (no finer skill breakdown authored yet) —
    each domain doubles as its own single skill. Shared by every subject that
    only has a trimester->domain-name list so far, not a full JSON curriculum."""
    subject = subjects[subject_code]
    for level_code, trimesters in skeleton.items():
        level = levels[level_code]
        if CurriculumDomain.query.filter_by(level_id=level.id, subject_id=subject.id).first():
            continue

        domain_trimesters = {}
        domain_order = {}
        for trimester, names in trimesters.items():
            for name in names:
                domain_trimesters.setdefault(name, []).append(trimester)
                domain_order.setdefault(name, len(domain_order))

        for name, sort_order in domain_order.items():
            code = slugify(name)
            domain = CurriculumDomain(
                level_id=level.id,
                subject_id=subject.id,
                code=code,
                name_fr=name,
                name_ar=name,  # no Arabic label authored yet for these levels
                sort_order=sort_order,
            )
            db.session.add(domain)
            db.session.flush()

            for trimester in domain_trimesters[name]:
                db.session.add(CurriculumDomainTrimester(domain_id=domain.id, trimester=trimester))

            db.session.add(
                CurriculumSkill(domain_id=domain.id, code=code, name_fr=name, name_ar=name, sort_order=0)
            )

    db.session.commit()


def main():
    with app.app_context():
        db.create_all()
        levels, subjects = seed_levels_and_subjects()
        seed_domain_curriculum(levels, subjects, "1", "math", MATH1_CURRICULUM_PATH, MATH1_TRIMESTERS)
        seed_skeleton_curriculum(levels, subjects, "math", MATH_SKELETON)
        seed_domain_curriculum(levels, subjects, "1", "ar", ARABIC1_CURRICULUM_PATH, ARABIC1_TRIMESTERS)
        seed_domain_curriculum(levels, subjects, "1", "science", SCIENCE1_CURRICULUM_PATH, SCIENCE1_TRIMESTERS)
        seed_skeleton_curriculum(levels, subjects, "science", SCIENCE_SKELETON)
        print("Seed complete.")


if __name__ == "__main__":
    main()
