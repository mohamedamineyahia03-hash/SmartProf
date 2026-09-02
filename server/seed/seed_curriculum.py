"""One-time/idempotent import of curriculum data into the generalized DB schema.

Full-detail curriculum (domains -> skills -> exercise_formats, bilingual)
exists for level 1 of Math, Arabic, Science, Français, and Anglais. All five
subjects also have a domain-only skeleton for levels 2-6 (each domain
doubles as its own single skill — no finer breakdown authored yet). Level 6
is the last year of Tunisian primary school and ends with the Concours
National de la 6ème: Math, Science, Arabe, and Français dedicate their T3
skeleton to revision + a "Concours blanc" (mock exam) track instead of new
material. Anglais gets a revision-only T3 at level 6 (its place in the
actual concours exam isn't confirmed, so no "Concours blanc" label is
claimed for it).

The levels 2-6 skeleton domain names for Math/Science/Arabe/Français/Anglais
(minus the T3 revision convention above) come from the official trimester
breakdown supplied by the user (programme_officiel_tunisie_2e_6e_complet.xlsx,
2026-09-02): one program summary per (level, subject), NOT differentiated
per trimester in the source — the same text is repeated for T1/T2/T3 — so
the domain lists below are intentionally identical across all three
trimesters for a given level/subject, rather than inventing a progression
the source doesn't state. Anglais/Français levels not covered by that
source (Anglais 2-4, Français 2) keep their earlier hand-authored skeleton,
since SmartProf offers them as an early paid enrichment ahead of where the
official programme introduces them (see SUBJECTS free_levels below).
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
    ("6", "6ème année", "السنة السادسة"),  # last year of primary — Concours National de la 6ème
]

ALL_LEVELS = ["1", "2", "3", "4", "5", "6"]

# code, label_fr, label_ar, free_levels
SUBJECTS = [
    ("math", "Mathématiques", "الرياضيات", ALL_LEVELS),
    ("science", "Éveil scientifique", "الإيقاظ العلمي", ALL_LEVELS),
    ("ar", "Arabe", "العربية", ALL_LEVELS),
    ("fr", "Français", "الفرنسية", ["3", "4", "5", "6"]),
    ("en", "Anglais", "الإنجليزية", ["4", "5", "6"]),  # paid unlock at levels 1-2-3
]

MATH_SKELETON = {
    "2": {
        "T1": ["Nombres jusqu'à 99", "Additions et soustractions simples", "Géométrie de base"],
        "T2": ["Nombres jusqu'à 99", "Additions et soustractions simples", "Géométrie de base"],
        "T3": ["Nombres jusqu'à 99", "Additions et soustractions simples", "Géométrie de base"],
    },
    "3": {
        "T1": ["Nombres jusqu'à 999", "Technique de l'addition posée", "Technique de la soustraction posée"],
        "T2": ["Nombres jusqu'à 999", "Technique de l'addition posée", "Technique de la soustraction posée"],
        "T3": ["Nombres jusqu'à 999", "Technique de l'addition posée", "Technique de la soustraction posée"],
    },
    "4": {
        "T1": ["Introduction à la multiplication", "Grands nombres", "Mesures de longueur et masses"],
        "T2": ["Introduction à la multiplication", "Grands nombres", "Mesures de longueur et masses"],
        "T3": ["Introduction à la multiplication", "Grands nombres", "Mesures de longueur et masses"],
    },
    "5": {
        "T1": ["Division", "Nombres décimaux", "Périmètres et aires", "Proportionnalité"],
        "T2": ["Division", "Nombres décimaux", "Périmètres et aires", "Proportionnalité"],
        "T3": ["Division", "Nombres décimaux", "Périmètres et aires", "Proportionnalité"],
    },
    "6": {
        "T1": ["Fractions", "Pourcentages", "Géométrie avancée (cercle, triangles)", "Situations-problèmes globales"],
        "T2": ["Fractions", "Pourcentages", "Géométrie avancée (cercle, triangles)", "Situations-problèmes globales"],
        "T3": ["Révision générale", "Concours blanc"],
    },
}

# Level 1 Math domain -> trimester(s), refined against the official Tunisia
# 2025/2026 trimester breakdown: T1 also covers basic spatial positioning
# (repérage gauche/droite, haut/bas), and numeration/calcul now extend into
# T3 for the "dizaine" (tens/units, numbers 10-19) and vertical-addition
# content introduced there — a domain still spans every trimester it has
# real content for, since trimester tagging is domain-level, not per-skill.
MATH1_TRIMESTERS = {
    "T1": ["pre_numeric", "numeration", "calcul", "espace_geometrie"],
    "T2": ["numeration", "calcul", "mesure", "problemes"],
    "T3": ["numeration", "calcul", "espace_geometrie", "mesure", "problemes"],
}

# Level 1 Arabic domain -> trimester(s): letters first, reading from T2,
# comprehension/expression/writing consolidated in T3.
ARABIC1_TRIMESTERS = {
    "T1": ["huruf"],
    "T2": ["huruf", "qiraa"],
    "T3": ["qiraa", "fahm", "kitaba"],
}
# "expression_orale_ecrite" (ex-"taabir") isn't listed above on purpose: its
# category is "expression" now, an independent section outside the
# trimester tree — see seed_domain_curriculum, which skips trimester
# assignment entirely for that category.

SCIENCE_SKELETON = {
    "2": {
        "T1": ["Le corps", "Les sens", "Les animaux et plantes de l'environnement proche"],
        "T2": ["Le corps", "Les sens", "Les animaux et plantes de l'environnement proche"],
        "T3": ["Le corps", "Les sens", "Les animaux et plantes de l'environnement proche"],
    },
    "3": {
        "T1": ["L'eau", "L'air", "Classification du vivant", "Hygiène de vie"],
        "T2": ["L'eau", "L'air", "Classification du vivant", "Hygiène de vie"],
        "T3": ["L'eau", "L'air", "Classification du vivant", "Hygiène de vie"],
    },
    "4": {
        "T1": ["Les états de la matière", "Le système digestif", "Écosystèmes"],
        "T2": ["Les états de la matière", "Le système digestif", "Écosystèmes"],
        "T3": ["Les états de la matière", "Le système digestif", "Écosystèmes"],
    },
    "5": {
        "T1": ["La respiration", "La circulation sanguine", "L'électricité de base", "L'environnement"],
        "T2": ["La respiration", "La circulation sanguine", "L'électricité de base", "L'environnement"],
        "T3": ["La respiration", "La circulation sanguine", "L'électricité de base", "L'environnement"],
    },
    "6": {
        "T1": ["Reproduction", "Écosystèmes", "Énergie"],
        "T2": ["Reproduction", "Écosystèmes", "Énergie"],
        "T3": ["Révision générale", "Concours blanc"],
    },
}

# Level 1 Science domain -> trimester(s): the body and living things first,
# surroundings/water mid-year, seasons wrap up the year.
SCIENCE1_TRIMESTERS = {
    "T1": ["corps_humain", "etres_vivants"],
    "T2": ["etres_vivants", "environnement", "eau"],
    "T3": ["eau", "saisons"],
}

# Levels 2-6 (level 1 has full-detail curriculum instead — see ARABIC1_TRIMESTERS
# above). Previously missing entirely; added from the official trimester
# breakdown (2026-09-02, see module docstring).
ARABIC_SKELETON = {
    "2": {
        "T1": ["Lecture", "Écriture", "Structures de base", "Expression orale"],
        "T2": ["Lecture", "Écriture", "Structures de base", "Expression orale"],
        "T3": ["Lecture", "Écriture", "Structures de base", "Expression orale"],
    },
    "3": {
        "T1": ["Étude de texte", "Enrichissement du vocabulaire", "Grammaire de base"],
        "T2": ["Étude de texte", "Enrichissement du vocabulaire", "Grammaire de base"],
        "T3": ["Étude de texte", "Enrichissement du vocabulaire", "Grammaire de base"],
    },
    "4": {
        "T1": ["Production écrite guidée", "Conjugaison (passé/présent)", "Grammaire approfondie"],
        "T2": ["Production écrite guidée", "Conjugaison (passé/présent)", "Grammaire approfondie"],
        "T3": ["Production écrite guidée", "Conjugaison (passé/présent)", "Grammaire approfondie"],
    },
    "5": {
        "T1": ["Expression écrite complexe", "Analyse grammaticale", "Orthographe grammaticale"],
        "T2": ["Expression écrite complexe", "Analyse grammaticale", "Orthographe grammaticale"],
        "T3": ["Expression écrite complexe", "Analyse grammaticale", "Orthographe grammaticale"],
    },
    "6": {
        "T1": ["Synthèse", "Analyse littéraire et dissertation", "Préparation au concours (C6)"],
        "T2": ["Synthèse", "Analyse littéraire et dissertation", "Préparation au concours (C6)"],
        "T3": ["Révision générale", "Concours blanc"],
    },
}

# Level 2 isn't in the official breakdown (Français starts at level 3 there)
# but stays hand-authored — SmartProf sells Français as an early paid
# enrichment at levels 1-2 ahead of where the programme itself introduces it.
FR_SKELETON = {
    "2": {
        "T1": ["Lecture", "Écriture", "Vocabulaire"],
        "T2": ["Grammaire", "Orthographe", "Vocabulaire"],
        "T3": ["Conjugaison", "Expression écrite"],
    },
    "3": {
        "T1": ["Découverte de la langue", "Graphie-phonie", "Lexique thématique", "Premiers dialogues"],
        "T2": ["Découverte de la langue", "Graphie-phonie", "Lexique thématique", "Premiers dialogues"],
        "T3": ["Découverte de la langue", "Graphie-phonie", "Lexique thématique", "Premiers dialogues"],
    },
    "4": {
        "T1": ["Lecture suivie", "Grammaire (nom, verbe, déterminants)", "Production de phrases"],
        "T2": ["Lecture suivie", "Grammaire (nom, verbe, déterminants)", "Production de phrases"],
        "T3": ["Lecture suivie", "Grammaire (nom, verbe, déterminants)", "Production de phrases"],
    },
    "5": {
        "T1": ["Textes narratifs", "Conjugaison (présent, futur, imparfait)", "Vocabulaire contextuel"],
        "T2": ["Textes narratifs", "Conjugaison (présent, futur, imparfait)", "Vocabulaire contextuel"],
        "T3": ["Textes narratifs", "Conjugaison (présent, futur, imparfait)", "Vocabulaire contextuel"],
    },
    "6": {
        "T1": ["Compréhension de textes élaborés", "Grammaire experte", "Production écrite structurée"],
        "T2": ["Compréhension de textes élaborés", "Grammaire experte", "Production écrite structurée"],
        "T3": ["Révision générale", "Concours blanc"],
    },
}

# Levels 2-4 aren't in the official breakdown (Anglais starts at level 5
# there) but stay hand-authored, same reasoning as Français level 2 above —
# an early paid enrichment product, not a claim about the school programme.
EN_SKELETON = {
    "2": {
        "T1": ["Vocabulary", "Grammar basics"],
        "T2": ["Listening & speaking", "Reading"],
        "T3": ["Writing", "Vocabulary"],
    },
    "3": {
        "T1": ["Vocabulary", "Grammar"],
        "T2": ["Reading comprehension", "Listening & speaking"],
        "T3": ["Writing", "Grammar"],
    },
    "4": {
        "T1": ["Vocabulary", "Grammar"],
        "T2": ["Reading comprehension", "Listening & speaking"],
        "T3": ["Writing", "Grammar"],
    },
    "5": {
        "T1": ["Initiation", "Salutations et alphabet", "Couleurs et nombres", "Objets de la classe", "Verbes d'action"],
        "T2": ["Initiation", "Salutations et alphabet", "Couleurs et nombres", "Objets de la classe", "Verbes d'action"],
        "T3": ["Initiation", "Salutations et alphabet", "Couleurs et nombres", "Objets de la classe", "Verbes d'action"],
    },
    "6": {
        "T1": ["Expression de soi", "Loisirs et famille", "Temps simples (grammar tenses)", "Dialogues de la vie quotidienne"],
        "T2": ["Expression de soi", "Loisirs et famille", "Temps simples (grammar tenses)", "Dialogues de la vie quotidienne"],
        "T3": ["Révision générale"],
    },
}

# Level 1 Français domain -> trimester(s): letters/reading and writing start
# together, vocabulary joins mid-year, grammar/orthographe and oral expression
# consolidate in T3 — same shape as Arabic1.
FR1_TRIMESTERS = {
    "T1": ["lecture_dechiffrage", "ecriture"],
    "T2": ["lecture_dechiffrage", "vocabulaire", "ecriture"],
    "T3": ["grammaire_orthographe", "vocabulaire"],
}
# "expression_orale_ecrite" and "recitation" aren't listed above on
# purpose: their category is "expression", an independent section outside
# the trimester tree — see seed_domain_curriculum.

# Level 1 Anglais domain -> trimester(s): alphabet/phonics and basic
# vocabulary first, listening/reading join mid-year, reading/writing/
# vocabulary consolidate in T3.
EN1_TRIMESTERS = {
    "T1": ["alphabet_phonics", "vocabulary_basics"],
    "T2": ["alphabet_phonics", "listening_speaking", "reading_basics"],
    "T3": ["reading_basics", "writing_basics", "vocabulary_basics"],
}

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MATH1_CURRICULUM_PATH = os.path.join(REPO_ROOT, "data", "math1", "math1_curriculum.json")
ARABIC1_CURRICULUM_PATH = os.path.join(REPO_ROOT, "data", "arabic1", "arabic1_curriculum.json")
SCIENCE1_CURRICULUM_PATH = os.path.join(REPO_ROOT, "data", "science1", "science1_curriculum.json")
FR1_CURRICULUM_PATH = os.path.join(REPO_ROOT, "data", "fr1", "fr1_curriculum.json")
EN1_CURRICULUM_PATH = os.path.join(REPO_ROOT, "data", "en1", "en1_curriculum.json")


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
        category = domain_data.get("category", "programme")
        domain = CurriculumDomain(
            level_id=level.id,
            subject_id=subject.id,
            code=domain_data["id"],
            name_fr=domain_data["name_fr"],
            name_ar=domain_data["name_ar"],
            sort_order=sort_order,
            category=category,
        )
        db.session.add(domain)
        db.session.flush()

        # "expression" sections (Expression orale et écrite, Récitation) are
        # independent of the trimester tree — no CurriculumDomainTrimester
        # rows at all, not even a default one.
        if category == "programme":
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
        seed_skeleton_curriculum(levels, subjects, "ar", ARABIC_SKELETON)
        seed_domain_curriculum(levels, subjects, "1", "science", SCIENCE1_CURRICULUM_PATH, SCIENCE1_TRIMESTERS)
        seed_skeleton_curriculum(levels, subjects, "science", SCIENCE_SKELETON)
        seed_domain_curriculum(levels, subjects, "1", "fr", FR1_CURRICULUM_PATH, FR1_TRIMESTERS)
        seed_skeleton_curriculum(levels, subjects, "fr", FR_SKELETON)
        seed_domain_curriculum(levels, subjects, "1", "en", EN1_CURRICULUM_PATH, EN1_TRIMESTERS)
        seed_skeleton_curriculum(levels, subjects, "en", EN_SKELETON)
        print("Seed complete.")


if __name__ == "__main__":
    main()
