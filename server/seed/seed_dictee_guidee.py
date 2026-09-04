"""Adds the "Dictee guidee" curriculum domain -- the listen-and-write
literacy space that replaces the deleted Recitation domain (see
_local-work memory: project_dictee_guidee_spec.md for the full design).

Scope confirmed with the user 2026-09-04: NOT a universal level 1-6
section. It lives only under the four paid contexts where it was asked
for -- Francais niveau 1, Francais niveau 2, Anglais niveau 1, Anglais
niveau 2. It also appears inside "L'Academie du Francais" and
"The English Academy" for free, because those Academies simply re-serve
this same niveau 1/2 content relabelled "Niveau 1"/"Niveau 2" -- no
duplicate domain needed there.

category="expression" (independent of the trimester tree, same pattern as
production_ecrite) -- this is a standing practice space, not tied to a
trimester's programme.

Four skills, one skill = one rubric, each mapped to its own exercise_format
so the frontend can dispatch on ex.format like it already does for
"recitation":
  - alphabet          -> lecon_lettres   (the 26-letter sequence + 60 extra
                                            mots-reperes, one exercise)
  - syllabe           -> lecon_syllabes  (syllable drills, one exercise)
  - mots_simples      -> lecon_mots      (word-building by theme, one exercise)
  - ecoute_ecriture   -> ecoute_ecriture (free write + hear-what-you-wrote,
                                            one exercise, no fixed content)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # server/

from app import app  # noqa: E402
from db import db  # noqa: E402
from models import CurriculumDomain, CurriculumExerciseFormat, CurriculumLevel, CurriculumSkill, CurriculumSubject  # noqa: E402

SKILLS = [
    ("alphabet", "Alphabet", "الأبجدية", "lecon_lettres"),
    ("syllabe", "Syllabe", "المقطع الصوتي", "lecon_syllabes"),
    ("mots_simples", "Mots simples", "كلمات بسيطة", "lecon_mots"),
    ("ecoute_ecriture", "Ecris et ecoute", "اكتب واستمع", "ecoute_ecriture"),
]

TARGETS = [
    ("1", "fr", "Dictee guidee", "الإملاء الموجّه"),
    ("2", "fr", "Dictee guidee", "الإملاء الموجّه"),
    ("1", "en", "Dictee guidee", "الإملاء الموجّه"),
    ("2", "en", "Dictee guidee", "الإملاء الموجّه"),
]


def main():
    with app.app_context():
        created = []
        for level_code, subject_code, name_fr, name_ar in TARGETS:
            level = CurriculumLevel.query.filter_by(code=level_code).first()
            subject = CurriculumSubject.query.filter_by(code=subject_code).first()
            if level is None or subject is None:
                print(f"! missing level/subject row for {level_code}/{subject_code} -- skipped")
                continue

            existing = CurriculumDomain.query.filter_by(
                level_id=level.id, subject_id=subject.id, code="dictee_guidee"
            ).first()
            if existing is not None:
                print(f"{level_code}/{subject_code}: dictee_guidee already exists, skipping")
                continue

            max_sort = (
                db.session.query(db.func.max(CurriculumDomain.sort_order))
                .filter_by(level_id=level.id, subject_id=subject.id)
                .scalar()
                or 0
            )
            domain = CurriculumDomain(
                level_id=level.id,
                subject_id=subject.id,
                code="dictee_guidee",
                name_fr=name_fr,
                name_ar=name_ar,
                sort_order=max_sort + 1,
                category="expression",
                is_exam=False,
            )
            db.session.add(domain)
            db.session.flush()

            for sort_order, (skill_code, skill_name_fr, skill_name_ar, format_code) in enumerate(SKILLS):
                skill = CurriculumSkill(
                    domain_id=domain.id,
                    code=skill_code,
                    name_fr=skill_name_fr,
                    name_ar=skill_name_ar,
                    sort_order=sort_order,
                )
                db.session.add(skill)
                db.session.flush()
                db.session.add(CurriculumExerciseFormat(skill_id=skill.id, format_code=format_code))

            db.session.commit()
            created.append(f"{level_code}/{subject_code}")
            print(f"{level_code}/{subject_code}: dictee_guidee created (4 skills)")

        print(f"\nDone: {len(created)} domain(s) created.")


if __name__ == "__main__":
    main()
